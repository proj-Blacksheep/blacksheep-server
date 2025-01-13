"""User model usage API module.

This module provides endpoints for retrieving user model usage statistics.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.authentication import get_current_user
from src.core.di import get_db, get_user_repository
from src.repositories.users import UserRepository
from src.schemas.v1.users import UserDTO
from src.services.user_model_usage import get_usage_by_user_name_and_date_range

router = APIRouter(
    prefix="/usage",
    tags=["usage"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{username}", response_model=dict)
async def get_user_usage(
    username: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserDTO = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> dict:
    """Get user's API usage statistics.

    Args:
        username: Username to get usage for.
        start_date: Optional start date for filtering usage records.
        end_date: Optional end date for filtering usage records.
        current_user: Current authenticated user.
        user_repository: User repository instance.

    Returns:
        dict: User's API usage statistics.

    Raises:
        HTTPException: If user is not authorized or not found.
    """
    if not current_user.is_admin and current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    async with get_db() as db:
        user = await user_repository.get_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        usage = await get_usage_by_user_name_and_date_range(
            username, start_date, end_date
        )

        return {
            "username": str(user.username),
            "current_usage": usage,
            "period": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
            },
        }
