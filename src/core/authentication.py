"""Authentication module.

This module provides functions for user authentication and token management.
"""

from datetime import UTC, datetime, timedelta
from typing import Any, Dict, Optional, cast

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.di import get_db, get_user_repository
from src.repositories.users import UserRepository
from src.schemas.v1.login import TokenData
from src.schemas.v1.users import UserDTO

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login", scheme_name="OAuth2", description="JWT token authentication"
)


async def authenticate_user(
    username: str,
    password: str,
    db: AsyncSession,
    user_repository: UserRepository,
) -> Optional[UserDTO]:
    """Authenticate a user with username and password.

    Args:
        username: The username to authenticate.
        password: The password to verify.
        db: Database session.
        user_repository: User repository instance.

    Returns:
        Optional[UserDTO]: Authenticated user DTO or None if authentication fails.
    """
    # 입력값 정리
    username = username.strip()  # 앞뒤 공백 제거
    username = "".join(c for c in username if c.isprintable())

    user = await user_repository.get_by_username(db, username)
    if user is None:
        return None

    if str(user.password) == password:  # TODO: 비밀번호 해싱 검증 필요
        return UserDTO.model_validate(user)
    return None


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
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


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserDTO:
    """Get current user from JWT token.

    Args:
        token: JWT token from request.
        user_repository: User repository instance.

    Returns:
        UserDTO: Current authenticated user.

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

    async with get_db() as db:
        user = await user_repository.get_by_username(db, token_data.username)
        if user is None:
            raise credentials_exception

        return UserDTO.model_validate(user)
