import re
from app.services.ai_service import ask_ai

async def ai_score(context: dict) -> int:
    prompt = f"""
Avalie o potencial de contratação deste lead de 0 a 100.
Considere clareza da dor, urgência e valor percebido.

Contexto:
{context}
"""
    response = await ask_ai(prompt)
    match = re.search(r"\d+", response)
    return int(match.group()) if match else 0

def rule_based_score(data: dict) -> int:
    score = 0

    if data.get("empresa"):
        score += 10
    if data.get("whatsapp"):
        score += 15
    if data.get("interesse"):
        score += 20

    if data.get("urgencia") == "alta":
        score += 20
    if data.get("orcamento") == "sim":
        score += 20

    return score