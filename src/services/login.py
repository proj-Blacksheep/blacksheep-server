from datetime import datetime, timedelta, UTC
from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status
from src.core.config import settings
from src.models.users import UserSchema
from sqlalchemy import select
from src.db.database import async_session_maker
from src.models.users import Users

# 이 값들은 환경변수로 관리하는 것이 좋습니다
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


async def authenticate_user(username: str, password: str) -> UserSchema | None:
    """Authenticate a user with username and password.

    Args:
        username: The username to authenticate.
        password: The password to verify.

    Returns:
        UserSchema | None: Authenticated user or None if authentication fails.
    """
    async with async_session_maker() as session:
        async with session.begin():
            query = select(Users).where(Users.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user is None:
                return None

            if str(user.password) != password:
                return None

            return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.

    Args:
        data: Dictionary containing claims to be encoded in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifies a JWT token and returns its payload.

    Args:
        token: JWT token to verify

    Returns:
        Dictionary containing the token claims

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
