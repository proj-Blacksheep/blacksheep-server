"""Login API endpoints module.

This module provides API endpoints for user authentication and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.authentication import authenticate_user, create_access_token
from src.models.models import Token

router = APIRouter(tags=["authentication"])


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Authenticate user and provide access token.

    Args:
        form_data: OAuth2 password request form containing username and password.

    Returns:
        Token: Access token for authenticated user.

    Raises:
        HTTPException: If authentication fails.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
