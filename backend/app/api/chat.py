import json
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.core.redis import redis_client
from app.core.config import settings

from app.services import ai_service, memory_service, lead_scoring, notification_service
from app.services.conversation_state import next_stage
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.schemas import ChatInput

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(data: ChatInput, db: AsyncSession = Depends(get_async_db)):
    logger.info(f"Received request for session_id: {data.session_id}")
    session_id = data.session_id

    # ===============================
    # 1️⃣ REDIS – recuperar estado
    # ===============================
    state_key = f"conversation:{session_id}"
    messages_key = f"messages:{session_id}"
    
    logger.info("Getting state from Redis...")
    raw_state = await redis_client.get(state_key)
    state = json.loads(raw_state) if raw_state else {
        "stage": "ENTRY",
        "collected_data": {},
        "lead_score": 0
    }
    logger.info(f"State retrieved: {state}")

    raw_messages = await redis_client.get(messages_key)
    messages_history = json.loads(raw_messages) if raw_messages else []
    logger.info("Message history retrieved.")

    # ===============================
    # 2️⃣ PREPARAR MENSAGENS PARA IA
    # ===============================
    messages_for_ai = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *messages_history,
        {"role": "user", "content": data.message}
    ]

    logger.info("Calling main AI service (get_ai_response)...")
    ai_data = await ai_service.get_ai_response(messages_for_ai)
    ai_reply = ai_data.get("reply", "Desculpe, não entendi.")
    logger.info("Main AI service call complete.")

    # ===============================
    # 2.1 EXTRAÇÃO DE DADOS (NER)
    # ===============================
    extracted = ai_data.get("extracted_data", {})
    if extracted:
        # Atualiza apenas os campos que vieram preenchidos (não nulos)
        clean_extracted = {k: v for k, v in extracted.items() if v}
        state["collected_data"].update(clean_extracted)
        logger.info(f"Data extracted and updated in state: {clean_extracted}")

    # ===============================
    # 3️⃣ ATUALIZAR HISTÓRICO (REDIS)
    # ===============================
    messages_history.append({"role": "user", "content": data.message})
    messages_history.append({"role": "assistant", "content": ai_reply})

    logger.info("Updating message history in Redis...")
    await redis_client.set(
        messages_key,
        json.dumps(messages_history),
        ex=3600
    )
    logger.info("Message history updated.")

    # ===============================
    # 4️⃣ STAGE + LEAD SCORING
    # ===============================
    state["stage"] = next_stage(state["stage"])
    logger.info(f"New stage: {state['stage']}")

    rule_score = lead_scoring.rule_based_score(state["collected_data"])
    
    logger.info("Calling scoring AI service (ai_score)...")
    ai_score_value = await lead_scoring.ai_score({
        "stage": state["stage"],
        "history": messages_history
    })
    logger.info(f"AI score received: {ai_score_value}")

    final_score = rule_score * 0.6 + ai_score_value * 0.4
    state["lead_score"] = final_score

    logger.info("Updating state in Redis...")
    await redis_client.set(
        state_key,
        json.dumps(state),
        ex=3600
    )
    logger.info("State updated in Redis.")

    # ===============================
    # 5️⃣ HANDOFF (WHATSAPP)
    # ===============================
    whatsapp_link = None
    if final_score >= 70 or ai_data.get("handoff"):
        whatsapp_link = f"https://wa.me/{settings.MY_WHATSAPP}"
        ai_reply += "\n\n🚀 Posso te conectar agora com um especialista humano no WhatsApp."
        
        # Dispara notificação para o Admin (Você)
        logger.info("Lead is hot! Sending notification...")
        await notification_service.notify_admin(state["collected_data"], final_score)

    # ===============================
    # 6️⃣ PERSISTIR NO MYSQL (SÓ NO CLOSE)
    # ===============================
    if state["stage"] == "CLOSE":
        logger.info("Stage is CLOSE, persisting to database...")
        lead = await memory_service.create_or_update_lead_from_state(
            db=db,
            session_id=session_id,
            state=state,
            resumo=ai_reply
        )
        logger.info(f"Lead {lead.id} persisted.")

        # limpeza opcional
        await redis_client.delete(state_key)
        await redis_client.delete(messages_key)
        logger.info("Redis keys deleted.")

    response_data = {
        "reply": ai_reply,
        "score": final_score,
        "whatsapp_link": whatsapp_link
    }
    logger.info(f"Returning response: {response_data}")
    return response_data
