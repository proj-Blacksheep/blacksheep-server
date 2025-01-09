"""Database configuration and session management module.

This module sets up the SQLAlchemy database connection and provides session management
functionality for the application.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, registry

# Create registry
mapper_registry = registry()

# Create declarative base
Base = declarative_base(metadata=mapper_registry.metadata)

# Database URL configuration
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# Create engine instance
engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Set to False in production
)

# Create async session maker
AsyncSessionLocal = AsyncSession(
    engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations.

    Yields:
        AsyncSession: The database session.

    Example:
        async with get_async_session() as session:
            result = await session.execute(query)
            await session.commit()
    """
    async with AsyncSessionLocal as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Initialize the database by creating all tables.

    This function should be called when the application starts.
    It will create all tables that don't exist yet.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
