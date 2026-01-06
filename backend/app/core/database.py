from typing import AsyncGenerator
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Note: The wait_for_db logic is now implicitly handled by startup events
# and the robust connection pooling of modern DB drivers.
# A manual wait script can be added to the Docker entrypoint if needed.

# Garante que a URL do banco use o driver assíncrono (aiomysql)
# usando o make_url do SQLAlchemy para uma abordagem mais robusta
db_url_obj = make_url(settings.DATABASE_URL)
if db_url_obj.drivername.startswith("mysql"):
    db_url_obj = db_url_obj.set(drivername="mysql+aiomysql")

async_engine = create_async_engine(db_url_obj, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session