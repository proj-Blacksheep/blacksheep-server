"""Dependency injection configuration module."""

from contextlib import asynccontextmanager
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.repositories.user_model_usage import (
    SQLAlchemyUserModelUsageRepository,
    UserModelUsageRepository,
)
from src.repositories.users import SQLAlchemyUserRepository, UserRepository


@lru_cache()
def get_user_repository() -> UserRepository:
    """Get the user repository instance.

    Returns:
        UserRepository: The user repository instance.
    """
    return SQLAlchemyUserRepository()


@lru_cache()
def get_user_model_usage_repository() -> UserModelUsageRepository:
    """Get the user model usage repository instance.

    Returns:
        UserModelUsageRepository: The user model usage repository instance.
    """
    return SQLAlchemyUserModelUsageRepository()


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get the database session.

    Yields:
        AsyncSession: The database session.

    Raises:
        DatabaseConnectionError: If connection to database fails.
        DatabaseError: If database operation fails.
    """
    async with get_session() as session:
        yield session
