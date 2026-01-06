from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Note: The wait_for_db logic is now implicitly handled by startup events
# and the robust connection pooling of modern DB drivers.
# A manual wait script can be added to the Docker entrypoint if needed.

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session