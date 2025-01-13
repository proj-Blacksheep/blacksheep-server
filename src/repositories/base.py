"""Base repository module for database operations."""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.base import Base

T = TypeVar("T", bound=Base)  # type: ignore


class BaseRepository(Generic[T]):
    """Base repository class for common database operations.

    Args:
        model: The SQLAlchemy model class to use for database operations.
    """

    def __init__(self, model: Type[T]):
        """Initialize the repository with a model class."""
        self._model = model

    async def create(self, session: AsyncSession, **kwargs) -> T:
        """Create a new record in the database.

        Args:
            session: The database session to use.
            **kwargs: The fields to set on the new record.

        Returns:
            The created record.
        """
        instance = self._model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def get_by_id(self, session: AsyncSession, record_id: int) -> Optional[T]:
        """Get a record by its ID.

        Args:
            session: The database session to use.
            record_id: The ID of the record to get.

        Returns:
            The record if found, None otherwise.
        """
        result = await session.execute(
            select(self._model).where(self._model.id == record_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession) -> List[T]:
        """Get all records.

        Args:
            session: The database session to use.

        Returns:
            List of all records.
        """
        result = await session.execute(select(self._model))
        return list(result.scalars().all())

    async def delete(self, session: AsyncSession, record_id: int) -> bool:
        """Delete a record by its ID.

        Args:
            session: The database session to use.
            record_id: The ID of the record to delete.

        Returns:
            True if the record was deleted, False if it wasn't found.
        """
        result = await session.execute(
            delete(self._model).where(self._model.id == record_id)
        )
        if result.rowcount > 0:
            await session.commit()
            return True
        return False
