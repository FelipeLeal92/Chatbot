from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    MY_WHATSAPP: str
    REDIS_URL: str
    NOTIFICATION_WEBHOOK_URL: str = ""

settings = Settings()

# Correção para o Render: O SQLAlchemy Async precisa do driver 'aiomysql' explícito.
# O Render fornece 'mysql://', então trocamos para 'mysql+aiomysql://' automaticamente.
if settings.DATABASE_URL.startswith("mysql://"):
    settings.DATABASE_URL = settings.DATABASE_URL.replace("mysql://", "mysql+aiomysql://")
