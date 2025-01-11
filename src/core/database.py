"""Database configuration module."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings
from src.db.models.base import Base


class DatabaseError(Exception):
    """Base exception for database related errors."""

    pass


class DatabaseConnectionError(DatabaseError):
    """Exception raised when database connection fails."""

    pass


class DatabaseInitializationError(DatabaseError):
    """Exception raised when database initialization fails."""

    pass


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,  # Enable connection health checks
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Initialize database tables.

    Creates all tables defined in the Base metadata.

    Raises:
        DatabaseInitializationError: If table creation fails.
    """
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as e:
        raise DatabaseInitializationError(
            f"Failed to initialize database: {str(e)}"
        ) from e


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session.

    Yields:
        AsyncSession: Database session for performing database operations.

    Raises:
        DatabaseConnectionError: If connection to database fails.
    """
    try:
        async with async_session() as session:
            try:
                yield session
            except SQLAlchemyError as e:
                await session.rollback()
                raise DatabaseError(f"Database operation failed: {str(e)}") from e
            finally:
                await session.close()
    except OperationalError as e:
        raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}") from e


async def check_database_connection() -> bool:
    """Check if database connection is healthy.

    Returns:
        bool: True if connection is successful, False otherwise.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False
