import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

async def notify_admin(lead_data: dict, score: int):
    """
    Envia um alerta para o Admin via Webhook (n8n, Zapier, CallMeBot) quando um lead é quente.
    """
    if not settings.NOTIFICATION_WEBHOOK_URL:
        return

    # Formata a mensagem para leitura humana
    message = (
        f"🔥 *LEAD QUENTE DETECTADO* (Score: {score})\n"
        f"👤 *Nome:* {lead_data.get('nome', 'Não informado')}\n"
        f"🏢 *Empresa:* {lead_data.get('empresa', 'Não informado')}\n"
        f"📞 *WhatsApp:* {lead_data.get('whatsapp', 'Não informado')}\n"
        f"💡 *Interesse:* {lead_data.get('interesse', 'Não informado')}"
    )

    payload = {
        "text": message,
        "score": score,
        "lead": lead_data
    }

    async with httpx.AsyncClient() as client:
        try:
            # Dispara e esquece (Fire and forget) para não travar o chat
            await client.post(settings.NOTIFICATION_WEBHOOK_URL, json=payload)
            logger.info(f"Notification sent to {settings.NOTIFICATION_WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")