"""User service module for business logic operations."""

from typing import Dict, List, Optional

from sqlalchemy import select

from src.core.database import get_session
from src.core.di import get_user_repository
from src.db.models.users import UserORM
from src.repositories.users import UserRepository
from src.schemas.v1.users import UserDTO
from src.services.user_model_usage import get_usage_by_user_name


class UserService:
    """Service for user-related operations."""

    def __init__(self, repository: UserRepository = get_user_repository()):
        """Initialize the user service.

        Args:
            repository: The user repository instance.
        """
        self._repository = repository

    async def create_user(
        self, username: str, password: str, is_admin: bool = False
    ) -> UserORM:
        """Create a new user.

        Args:
            username: The username for the new user.
            password: The password for the user account.
            is_admin: Whether the user is an admin. Defaults to False.

        Returns:
            The created user.

        Raises:
            ValueError: If user creation fails or user already exists.
        """
        async with get_session() as session:
            try:
                # 사용자 중복 체크
                existing_user = await self._repository.get_by_username(
                    session, username
                )
                if existing_user is not None:
                    raise ValueError(f"User {username} already exists")

                # 새 사용자 생성
                user = await self._repository.create_user(
                    session, username=username, password=password, is_admin=is_admin
                )
                await session.commit()
                await session.refresh(user)  # 생성된 사용자 정보를 새로고침
                return user
            except Exception:
                await session.rollback()
                raise

    async def get_all_users(self) -> List[UserORM]:
        """Get all users.

        Returns:
            List of all users.
        """
        async with get_session() as session:
            return await self._repository.get_all(session)

    async def get_user_by_api_key(self, api_key: str) -> Optional[UserDTO]:
        """Get user information from the database by API key.

        Args:
            api_key: The API key of the user.

        Returns:
            Optional[UserDTO]: The user DTO object if found, None otherwise.
        """
        async with get_session() as session:
            result = await session.execute(
                select(UserORM).where(UserORM.api_key == api_key)
            )
            user = result.scalar_one_or_none()
            if user:
                return UserDTO.model_validate(user)
            return None

    async def delete_user(self, username: str) -> bool:
        """Delete a user.

        Args:
            username: The username of the user to delete.

        Returns:
            True if the user was deleted, False if they weren't found.
        """
        async with get_session() as session:
            user = await self._repository.get_by_username(session, username)
            if user is None:
                return False

            result = await session.execute(select(user.id))
            user_id = result.scalar_one()
            return await self._repository.delete(session, user_id)

    async def set_usage_limit(self, username: str, limit: int) -> bool:
        """Set the usage limit for a user.

        Args:
            username: The username of the user.
            limit: The new usage limit.

        Returns:
            True if the limit was set, False if the user wasn't found.
        """
        async with get_session() as session:
            return await self._repository.set_usage_limit(session, username, limit)

    async def update_password(
        self, username: str, current_password: str, new_password: str
    ) -> bool:
        """Update a user's password.

        Args:
            username: The username of the user.
            current_password: The current password for verification.
            new_password: The new password to set.

        Returns:
            True if the password was updated, False if verification fails.
        """
        async with get_session() as session:
            return await self._repository.update_password(
                session, username, current_password, new_password
            )

    async def get_user_usage_stats(self, username: str) -> Dict:
        """Get usage statistics for a user.

        Args:
            username: The username to get statistics for.

        Returns:
            Dictionary containing usage statistics.

        Raises:
            ValueError: If the user is not found.
        """
        async with get_session() as session:
            user = await self._repository.get_by_username(session, username)
            if user is None:
                raise ValueError(f"User {username} not found")

        usage = await get_usage_by_user_name(username)
        return {"username": username, "usage": usage}
