"""User repository module for database operations."""

import uuid
from abc import abstractmethod
from typing import List, Optional, Protocol

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.users import UserORM
from src.repositories.base import BaseRepository


class UserRepository(Protocol):
    """Interface for user-related database operations."""

    @abstractmethod
    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> Optional[UserORM]:
        """Get a user by their username.

        Args:
            session: The database session to use.
            username: The username to search for.

        Returns:
            The user if found, None otherwise.
        """
        ...

    @abstractmethod
    async def get_by_api_key(
        self, session: AsyncSession, api_key: str
    ) -> Optional[UserORM]:
        """Get a user by their API key.

        Args:
            session: The database session to use.
            api_key: The API key to search for.

        Returns:
            The user if found, None otherwise.
        """
        ...

    @abstractmethod
    async def create_user(
        self,
        session: AsyncSession,
        username: str,
        password: str,
        is_admin: bool = False,
    ) -> UserORM:
        """Create a new user.

        Args:
            session: The database session to use.
            username: The username for the new user.
            password: The password for the user account.
            is_admin: Whether the user is an admin. Defaults to False.

        Returns:
            The created user.

        Raises:
            ValueError: If a user with the given username already exists.
        """
        ...

    @abstractmethod
    async def update_password(
        self,
        session: AsyncSession,
        username: str,
        current_password: str,
        new_password: str,
    ) -> bool:
        """Update a user's password.

        Args:
            session: The database session to use.
            username: The username of the user.
            current_password: The current password for verification.
            new_password: The new password to set.

        Returns:
            True if the password was updated, False otherwise.
        """
        ...

    @abstractmethod
    async def set_usage_limit(
        self, session: AsyncSession, username: str, limit: int
    ) -> bool:
        """Set the usage limit for a user.

        Args:
            session: The database session to use.
            username: The username of the user.
            limit: The new usage limit.

        Returns:
            True if the limit was set, False if the user wasn't found.
        """
        ...

    @abstractmethod
    async def get_all(self, session: AsyncSession) -> List[UserORM]:
        """Get all users.

        Args:
            session: The database session to use.

        Returns:
            List of all users.
        """
        ...

    @abstractmethod
    async def delete(self, session: AsyncSession, record_id: int) -> bool:
        """Delete a user by ID.

        Args:
            session: The database session to use.
            record_id: The ID of the user to delete.

        Returns:
            True if the user was deleted, False if not found.
        """
        ...


class SQLAlchemyUserRepository(BaseRepository[UserORM], UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self):
        """Initialize the user repository."""
        super().__init__(UserORM)

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> Optional[UserORM]:
        """Get a user by their username."""
        result = await session.execute(
            select(self._model).where(self._model.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_api_key(
        self, session: AsyncSession, api_key: str
    ) -> Optional[UserORM]:
        """Get a user by their API key."""
        result = await session.execute(
            select(self._model).where(self._model.api_key == api_key)
        )
        return result.scalar_one_or_none()

    async def create_user(
        self,
        session: AsyncSession,
        username: str,
        password: str,
        is_admin: bool = False,
    ) -> UserORM:
        """Create a new user."""
        user = self._model(
            username=username,
            password=password,
            api_key=str(uuid.uuid4().hex),
            is_admin=is_admin,
        )
        session.add(user)
        await session.flush()  # 데이터베이스에 변경사항을 반영하지만 커밋하지는 않음
        return user

    async def update_password(
        self,
        session: AsyncSession,
        username: str,
        current_password: str,
        new_password: str,
    ) -> bool:
        """Update a user's password."""
        user = await self.get_by_username(session, username)
        if (
            user is None or str(user.password) != current_password
        ):  # TODO: 비밀번호 해싱 검증 필요
            return False

        stmt = (
            update(self._model)
            .where(self._model.username == username)
            .values(password=new_password)  # TODO: 비밀번호 해싱 필요
        )
        await session.execute(stmt)
        await session.commit()
        return True

    async def set_usage_limit(
        self, session: AsyncSession, username: str, limit: int
    ) -> bool:
        """Set the usage limit for a user."""
        user = await self.get_by_username(session, username)
        if user is None:
            return False

        stmt = (
            update(self._model)
            .where(self._model.username == username)
            .values(usage_limit=limit)
        )
        await session.execute(stmt)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> List[UserORM]:
        """Get all users."""
        return await super().get_all(session)

    async def delete(self, session: AsyncSession, record_id: int) -> bool:
        """Delete a user by ID."""
        return await super().delete(session, record_id)
