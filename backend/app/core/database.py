from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Note: The wait_for_db logic is now implicitly handled by startup events
# and the robust connection pooling of modern DB drivers.
# A manual wait script can be added to the Docker entrypoint if needed.

# Garante que a URL do banco use o driver assíncrono (aiomysql)
# O Render/Provedores geralmente fornecem 'mysql://' que padroniza para sync (pymysql)
db_url = settings.DATABASE_URL
if db_url.startswith("mysql://"):
    db_url = db_url.replace("mysql://", "mysql+aiomysql://", 1)
elif db_url.startswith("mysql+pymysql://"):
    db_url = db_url.replace("mysql+pymysql://", "mysql+aiomysql://", 1)

async_engine = create_async_engine(db_url, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session