"""Database configuration module.

This module provides database connection and session management functionality.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import settings

Base = declarative_base()

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=settings.DB_ECHO, future=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session.

    Yields:
        AsyncSession: The database session.
    """
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()  # type: ignore[func-returns-value]
        raise
    finally:
        await session.close()  # type: ignore[func-returns-value]


async def init_db() -> None:
    """Initialize the database by creating all tables.

    This function should be called when the application starts.
    It will create all tables that don't exist yet.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
