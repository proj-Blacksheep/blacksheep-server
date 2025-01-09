from datetime import datetime, timedelta, UTC
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import select

from src.core.config import settings
from src.db.database import async_session_maker
from src.models.models import UserResponse
from src.models.users import Users, UserSchema


class TokenData(BaseModel):
    """Data structure for decoded token payload.

    Args:
        username: The username extracted from the token.
        exp: The expiration timestamp of the token.
    """

    username: str
    exp: datetime


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login", scheme_name="OAuth2", description="JWT token authentication"
)


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

            if user.password != password:  # TODO: 실제 구현시 비밀번호 해싱 필요
                return None

            return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token.

    Args:
        data: Dictionary containing claims to be encoded in the token.
        expires_delta: Optional expiration time delta.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verifies a JWT token and returns its payload.

    Args:
        token: JWT token to verify.

    Returns:
        dict: Dictionary containing the token claims.

    Raises:
        HTTPException: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    """Validates the JWT token and returns the current authenticated user.

    This function extracts the JWT token from the request headers, validates it,
    and returns the authenticated user information. It serves as a dependency
    for protected endpoints.

    Args:
        token: The JWT token from the request.

    Returns:
        Users: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid, expired, or the user is not found.
    """
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        async with async_session_maker() as session:
            async with session.begin():
                query = select(Users).where(Users.username == username)
                result = await session.execute(query)
                user = result.scalar_one_or_none()

                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not found",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                return user

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
