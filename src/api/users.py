"""User API endpoints module.

This module provides API endpoints for user management operations including
user creation, deletion, and updates.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from src.core.authentication import get_current_user
from src.db.database import get_session
from src.models.models import UserCreate, UserResponse
from src.models.users import Users
from src.services.user_model_usage import get_usage_by_user_name
from src.services.users import (
    create_user_db,
    delete_user,
    get_all_users,
    set_usage_limit,
    update_password,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user.

    Args:
        user: User creation request containing username, password, and role.

    Returns:
        UserResponse: Created user information.

    Raises:
        HTTPException: If user creation fails.
    """
    db_user = await create_user_db(user.username, user.password, user.role)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user",
        )
    return UserResponse(
        username=db_user.username,
        role=db_user.role,
        api_key=db_user.api_key,
    )


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Users = Depends(get_current_user),
) -> UserResponse:
    """Get current user information.

    Args:
        current_user: Current authenticated user.

    Returns:
        UserResponse: Current user information.
    """
    return UserResponse(
        username=current_user.username,
        role=current_user.role,
        api_key=current_user.api_key,
    )


@router.get("/all", response_model=list[UserResponse])
async def read_all_users(
    current_user: Users = Depends(get_current_user),
) -> list[UserResponse]:
    """Get all users information.

    Args:
        current_user: Current authenticated user.

    Returns:
        list[UserResponse]: List of all users information.

    Raises:
        HTTPException: If user is not authorized.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    users = await get_all_users()
    return [
        UserResponse(username=user.username, role=user.role, api_key=user.api_key)
        for user in users
    ]


@router.get("/usage/{username}", response_model=dict)
async def get_user_usage(
    username: str, current_user: Users = Depends(get_current_user)
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
    if current_user.role != "admin" and current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    async with get_session() as session:
        result = await session.execute(select(Users).where(Users.username == username))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    usage = await get_usage_by_user_name(username)
    return {"username": username, "usage": usage}


@router.post("/limit/{username}")
async def set_user_limit(
    username: str, limit: int, current_user: Users = Depends(get_current_user)
) -> dict:
    """Set usage limit for a user.

    Args:
        username: Username to set limit for.
        limit: New usage limit.
        current_user: Current authenticated user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If user is not authorized or operation fails.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    success = await set_usage_limit(username, limit)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"message": f"Usage limit for {username} set to {limit}"}


@router.delete("/{username}")
async def remove_user(
    username: str, current_user: Users = Depends(get_current_user)
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
    if current_user.role != "admin":
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
    current_user: Users = Depends(get_current_user),
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
