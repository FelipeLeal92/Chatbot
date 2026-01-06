from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    MY_WHATSAPP: str
    REDIS_URL: str
    NOTIFICATION_WEBHOOK_URL: str = ""

settings = Settings()
