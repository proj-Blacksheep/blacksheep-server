"""User management service module."""

import uuid
from typing import List, Optional, cast

from sqlalchemy import delete, select

from src.db.database import get_session
from src.models.users import Users


async def create_user_db(username: str, password: str, role: str = "basic") -> Users:
    """Create a new user in the database.

    Args:
        username: The username for the new user.
        password: The password for the user account.
        role: The role of the user (basic or admin). Defaults to basic.

    Returns:
        Users: The created or existing user object.

    Raises:
        ValueError: If user creation fails.
    """
    async with get_session() as session:
        # Check if username already exists
        result = await session.execute(select(Users).where(Users.username == username))
        user = result.scalar_one_or_none()
        if user:
            return cast(Users, user)

        api_key = str(uuid.uuid4().hex)
        new_user = Users(
            username=username,
            password=password,
            api_key=api_key,
            role=role,
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user


async def get_all_users() -> List[Users]:
    """Get all users from the database.

    Returns:
        List[Users]: List of all users in the database.
    """
    async with get_session() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        return list(users)


async def get_user_by_api_key(api_key: str) -> Optional[Users]:
    """Get a user by their API key.

    Args:
        api_key: The API key to search for.

    Returns:
        Optional[Users]: The user object if found, None otherwise.
    """
    async with get_session() as session:
        result = await session.execute(select(Users).where(Users.api_key == api_key))
        user = result.scalar_one_or_none()
        return cast(Optional[Users], user)


async def delete_user(username: str) -> bool:
    """Delete a user from the database.

    Args:
        username: The username of the user to delete.

    Returns:
        bool: True if user was deleted, False if user was not found.
    """
    async with get_session() as session:
        result = await session.execute(delete(Users).where(Users.username == username))
        if result.rowcount > 0:
            await session.commit()
            return True
        return False


async def set_usage_limit(username: str, limit: int) -> bool:
    """Set usage limit for a user.

    Args:
        username: The username of the user.
        limit: The new usage limit to set.

    Returns:
        bool: True if limit was set successfully, False if user was not found.
    """
    async with get_session() as session:
        result = await session.execute(select(Users).where(Users.username == username))
        user = result.scalar_one_or_none()

        if not user:
            return False

        user.usage_limit = limit
        await session.commit()
        return True


async def update_password(
    username: str, current_password: str, new_password: str
) -> bool:
    """Update user's password.

    Args:
        username: The username of the user.
        current_password: The current password for verification.
        new_password: The new password to set.

    Returns:
        bool: True if password was updated successfully, False if verification fails.
    """
    async with get_session() as session:
        result = await session.execute(select(Users).where(Users.username == username))
        user = result.scalar_one_or_none()

        if not user or user.password != current_password:  # TODO: 실제 구현시 비밀번호 해싱 필요
            return False

        user.password = new_password
        await session.commit()
        return True
