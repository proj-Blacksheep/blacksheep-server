"""User API endpoints module.

This module provides API endpoints for user management operations including
user creation, deletion, and updates.
"""

from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from src.core.authentication import get_current_user
from src.db.database import get_session
from src.schemas.v1.users import UserCreateRequest, UserDTO, UserMeResponse
from src.services.user_model_usage import get_usage_by_user_name
from src.services.users import (
    create_user_db,
    delete_user,
    get_all_users,
    get_user_usage_stats,
    set_usage_limit,
    update_password,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_user(user: UserCreateRequest) -> Dict[str, str]:
    """Create a new user.

    Args:
        user: User creation request containing username, password, and role.

    Returns:
        UserResponse: Created user information.

    Raises:
        HTTPException: If user creation fails.
    """
    db_user = await create_user_db(
        username=user.username,
        password=user.password,
        is_admin=user.is_admin,
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user",
        )
    return {"message": f"User {db_user.username} created successfully"}


@router.get("/me", response_model=UserMeResponse)
async def read_users_me(
    current_user: UserDTO = Depends(get_current_user),
) -> UserMeResponse:
    """Get current user information.

    Args:
        current_user: Current authenticated user.

    Returns:
        UserResponse: Current user information.
    """
    return UserMeResponse(
        username=current_user.username,
        api_key=current_user.api_key,
        is_admin=current_user.is_admin,
    )


@router.get("/all", response_model=list[UserMeResponse])
async def read_all_users(
    current_user: UserDTO = Depends(get_current_user),
) -> list[UserMeResponse]:
    """Get all users information.

    Args:
        current_user: Current authenticated user.

    Returns:
        list[UserResponse]: List of all users information.

    Raises:
        HTTPException: If user is not authorized.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    users = await get_all_users()
    return [
        UserMeResponse(
            username=user.username, is_admin=user.is_admin, api_key=user.api_key
        )
        for user in users
    ]


@router.get("/usage/{username}", response_model=dict)
async def get_user_usage(
    username: str, current_user: UserDTO = Depends(get_current_user)
) -> dict:
    """Get user's API usage statistics.

    Args:
        username: Username to get usage for.
        current_user: Current authenticated user.

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

    try:
        return await get_user_usage_stats(username)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete("/{username}")
async def remove_user(
    username: str, current_user: UserDTO = Depends(get_current_user)
) -> dict:
    """Delete a user.

    Args:
        username: Username to delete.
        current_user: Current authenticated user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If user is not authorized or operation fails.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    success = await delete_user(username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"message": f"User {username} deleted successfully"}


@router.post("/password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: UserDTO = Depends(get_current_user),
) -> dict:
    """Change user's password.

    Args:
        current_password: Current password for verification.
        new_password: New password to set.
        current_user: Current authenticated user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If password change fails.
    """
    success = await update_password(
        str(current_user.username), current_password, new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password",
        )

    return {"message": "Password updated successfully"}
