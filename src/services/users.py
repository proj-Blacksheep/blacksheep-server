from typing import List
from src.db.database import async_session_maker
from src.models.users import Users
import uuid
from sqlalchemy import select


async def create_user_db(username: str, password: str) -> Users:
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
            role="basic",  # 기본 역할을 'basic'으로 설정
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
