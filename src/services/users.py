from typing import List
from src.db.database import async_session_maker
from src.models.users import Users
import uuid
from sqlalchemy import select


async def create_user_db(username: str, password: str, role: str = "basic") -> Users:
    """Create a new user in the database.

    Args:
        username: The username for the new user.
        password: The password for the user account.

    Returns:
        Users: The created user object.
    """
    async with async_session_maker() as session:
        api_key = str(uuid.uuid4().hex)  # 32자리 랜덤 문자열 생성

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
    async with async_session_maker() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        return list(users)


async def get_user_by_api_key(api_key: str) -> Users | None:
    """Get a user by their API key.

    Args:
        api_key: The API key to search for.

    Returns:
        Users | None: The user object if found, None otherwise.
    """
    async with async_session_maker() as session:
        result = await session.execute(select(Users).where(Users.api_key == api_key))
        return result.scalar_one_or_none()


async def get_api_key_by_credentials(username: str, password: str) -> str | None:
    """Get user's API key using their username and password.

    Args:
        username: The username of the user.
        password: The password of the user.

    Returns:
        str | None: The API key if credentials are valid, None otherwise.
    """
    async with async_session_maker() as session:
        result = await session.execute(
            select(Users).where(Users.username == username, Users.password == password)
        )
        user = result.scalar_one_or_none()
        return str(user.api_key) if user else None
