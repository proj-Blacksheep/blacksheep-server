"""User API endpoints module.

This module provides API endpoints for user management operations including
user creation, deletion, and updates.
"""

from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.authentication import get_current_user
from src.core.di import get_db, get_user_repository
from src.repositories.users import UserRepository
from src.schemas.v1.users import UserCreateRequest, UserDTO, UserMeResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_user(
    user: UserCreateRequest,
    user_repository: UserRepository = Depends(get_user_repository),
) -> Dict[str, str]:
    """Create a new user.

    Args:
        user: User creation request containing username, password, and role.
        user_repository: User repository instance.

    Returns:
        Dict[str, str]: Success message.

    Raises:
        HTTPException: If user creation fails.
    """
    try:
        async with get_db() as db:
            # 먼저 사용자가 이미 존재하는지 확인
            existing_user = await user_repository.get_by_username(db, user.username)
            if existing_user is not None:
                raise ValueError("User already exists.")

            # 새 사용자 생성
            db_user = await user_repository.create_user(
                db,
                username=user.username,
                password=user.password,
                is_admin=user.is_admin,
            )
            await db.commit()  # 명시적으로 커밋
            return {"message": f"User {str(db_user.username)} created successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get("/me", response_model=UserMeResponse)
async def read_users_me(
    current_user: UserDTO = Depends(get_current_user),
) -> UserMeResponse:
    """Get current user information.

    Args:
        current_user: Current authenticated user.

    Returns:
        UserMeResponse: Current user information.
    """
    return UserMeResponse(
        username=str(current_user.username),
        api_key=str(current_user.api_key),
        is_admin=bool(current_user.is_admin),
    )


@router.get("/all", response_model=list[UserMeResponse])
async def read_all_users(
    current_user: UserDTO = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> list[UserMeResponse]:
    """Get all users information.

    Args:
        current_user: Current authenticated user.
        user_repository: User repository instance.

    Returns:
        list[UserMeResponse]: List of all users information.

    Raises:
        HTTPException: If user is not authorized.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    async with get_db() as db:
        users = await user_repository.get_all(db)
        return [
            UserMeResponse(
                username=str(user.username),
                is_admin=bool(user.is_admin),
                api_key=str(user.api_key),
            )
            for user in users
        ]


@router.get("/usage/{username}", response_model=dict)
async def get_user_usage(
    username: str,
    current_user: UserDTO = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> dict:
    """Get user's API usage statistics.

    Args:
        username: Username to get usage for.
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

        return {
            "username": str(user.username),
            "usage_limit": 0,
            "current_usage": 0,
        }


@router.delete("/{username}")
async def remove_user(
    username: str,
    current_user: UserDTO = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> dict:
    """Delete a user.

    Args:
        username: Username to delete.
        current_user: Current authenticated user.
        user_repository: User repository instance.

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

    async with get_db() as db:
        user = await user_repository.get_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await user_repository.delete(db, int(str(user.id)))
        return {"message": f"User {username} deleted successfully"}


@router.post("/password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: UserDTO = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> dict:
    """Change user's password.

    Args:
        current_password: Current password for verification.
        new_password: New password to set.
        current_user: Current authenticated user.
        user_repository: User repository instance.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If password change fails.
    """
    async with get_db() as db:
        success = await user_repository.update_password(
            db,
            str(current_user.username),
            current_password,
            new_password,
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid current password",
            )

        return {"message": "Password updated successfully"}
