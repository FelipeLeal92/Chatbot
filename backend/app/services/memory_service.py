from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lead import Lead

def classify_lead(score: int) -> str:
    if score >= 70:
        return "quente"
    if score >= 40:
        return "morno"
    return "frio"


async def create_or_update_lead_from_state(
    db: AsyncSession,
    session_id: str, # session_id might be useful for finding existing leads
    state: dict,
    resumo: str,
):
    """
    Persists the final lead state from Redis to the database.
    """
    collected_data = state.get("collected_data", {})
    lead_score = state.get("lead_score", 0)

    # Here you might want to find an existing lead by session_id if your model supports it
    # For now, we create a new one each time as per the new model structure.
    lead = Lead(
        nome=collected_data.get("nome"),
        empresa=collected_data.get("empresa"),
        whatsapp=collected_data.get("whatsapp"),
        dor_principal=collected_data.get("dor_principal"),
        interesse=str(collected_data.get("interesse")),
        lead_score=lead_score,
        status=classify_lead(lead_score),
        resumo_ia=resumo,
        origem="chat_widget"
    )

    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead

