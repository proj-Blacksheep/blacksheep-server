"""Login API endpoints module.

This module provides API endpoints for user authentication and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.authentication import authenticate_user, create_access_token
from src.core.di import get_db, get_user_repository
from src.repositories.users import UserRepository
from src.schemas.v1.login import Token

router = APIRouter(tags=["authentication"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(get_user_repository),
) -> Token:
    """Authenticate user and provide access token.

    Args:
        form_data: OAuth2 password request form containing username and password.
        user_repository: User repository instance.

    Returns:
        Token: Access token for authenticated user.

    Raises:
        HTTPException: If authentication fails.
    """

    async with get_db() as db:
        user = await authenticate_user(
            form_data.username, form_data.password, db, user_repository
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")
