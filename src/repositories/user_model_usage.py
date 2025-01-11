"""User model usage repository module."""

from abc import abstractmethod
from typing import List, Optional, Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user_model_usage import UserModelUsage
from src.repositories.base import BaseRepository


class UserModelUsageRepository(Protocol):
    """Interface for user model usage repository."""

    @abstractmethod
    async def get_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> List[UserModelUsage]:
        """Get all usage records for a user.

        Args:
            session: The database session to use.
            user_id: The ID of the user.

        Returns:
            List of usage records.
        """
        ...

    @abstractmethod
    async def get_by_user_and_model(
        self,
        session: AsyncSession,
        user_id: int,
        model_id: int,
        usage_type: str,
    ) -> Optional[UserModelUsage]:
        """Get usage record for a specific user and model.

        Args:
            session: The database session to use.
            user_id: The ID of the user.
            model_id: The ID of the model.
            usage_type: The type of usage.

        Returns:
            Usage record if found, None otherwise.
        """
        ...

    @abstractmethod
    async def create_or_update(
        self,
        session: AsyncSession,
        user_id: int,
        model_id: int,
        usage_type: str,
        count: int = 1,
    ) -> UserModelUsage:
        """Create or update a usage record.

        Args:
            session: The database session to use.
            user_id: The ID of the user.
            model_id: The ID of the model.
            usage_type: The type of usage.
            count: The number to increment usage by.

        Returns:
            The created or updated usage record.
        """
        ...


class SQLAlchemyUserModelUsageRepository(
    BaseRepository[UserModelUsage], UserModelUsageRepository
):
    """SQLAlchemy implementation of UserModelUsageRepository."""

    def __init__(self):
        """Initialize the repository."""
        super().__init__(UserModelUsage)

    async def get_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> List[UserModelUsage]:
        """Get all usage records for a user."""
        result = await session.execute(
            select(self._model).where(self._model.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_user_and_model(
        self,
        session: AsyncSession,
        user_id: int,
        model_id: int,
        usage_type: str,
    ) -> Optional[UserModelUsage]:
        """Get usage record for a specific user and model."""
        result = await session.execute(
            select(self._model).where(
                self._model.user_id == user_id,
                self._model.model_id == model_id,
                self._model.usage_type == usage_type,
            )
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        session: AsyncSession,
        user_id: int,
        model_id: int,
        usage_type: str,
        count: int = 1,
    ) -> UserModelUsage:
        """Create or update a usage record."""
        usage_record = await self.get_by_user_and_model(
            session, user_id, model_id, usage_type
        )

        if usage_record:
            usage_record.usage_count = usage_record.usage_count + count
        else:
            usage_record = await self.create(
                session,
                user_id=user_id,
                model_id=model_id,
                usage_type=usage_type,
                usage_count=count,
            )

        await session.commit()
        return usage_record
