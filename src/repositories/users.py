"""User repository module for database operations."""

import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import UserORM
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserORM]):
    """Repository for user-related database operations."""

    def __init__(self):
        """Initialize the user repository."""
        super().__init__(UserORM)

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
        result = await session.execute(
            select(self._model).where(self._model.username == username)
        )
        return result.scalar_one_or_none()

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
        existing_user = await self.get_by_username(session, username)
        if existing_user is not None:
            raise ValueError("User already exists.")

        return await self.create(
            session,
            username=username,
            password=password,  # TODO: 비밀번호 해싱 필요
            api_key=str(uuid.uuid4().hex),
            is_admin=is_admin,
        )

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
        """Set the usage limit for a user.

        Args:
            session: The database session to use.
            username: The username of the user.
            limit: The new usage limit.

        Returns:
            True if the limit was set, False if the user wasn't found.
        """
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
