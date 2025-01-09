"""Authentication module.

This module provides functions for user authentication and token management.
"""

from datetime import UTC, datetime, timedelta
from typing import Any, Optional, cast

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import select

from src.core.config import settings
from src.db.database import get_session
from src.models.users import Users


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


async def authenticate_user(username: str, password: str) -> Optional[Users]:
    """Authenticate a user with username and password.

    Args:
        username: The username to authenticate.
        password: The password to verify.

    Returns:
        Optional[Users]: Authenticated user or None if authentication fails.
    """
    async with get_session() as session:
        query = select(Users).where(Users.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        if user.password != password:  # TODO: 실제 구현시 비밀번호 해싱 필요
            return None

        return cast(Users, user)


def create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
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
    return str(encoded_jwt)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    """Get current user from JWT token.

    Args:
        token: JWT token from request.

    Returns:
        Users: Current authenticated user.

    Raises:
        HTTPException: If token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = cast(str, payload.get("sub"))
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, exp=payload.get("exp"))
    except jwt.InvalidTokenError:
        raise credentials_exception

    async with get_session() as session:
        result = await session.execute(
            select(Users).where(Users.username == token_data.username)
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
        return cast(Users, user)
