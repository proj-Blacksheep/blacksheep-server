from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.users import UserResponse, UserSchema, Users
from src.services.users import (
    create_user_db,
    get_all_users,
    delete_user,
    set_usage_limit,
    update_password,
)
from src.services.user_model_usage import get_usage_by_user_name
from src.core.authentication import get_current_user
from src.db.database import async_session_maker
from pydantic import BaseModel
import uuid
from sqlalchemy import select

router = APIRouter(prefix="/users", tags=["users"])


class UsageLimitRequest(BaseModel):
    username: str
    limit: int


class UpdatePasswordRequest(BaseModel):
    """Request model for password update.

    Attributes:
        current_password: The current password for verification.
        new_password: The new password to set.
    """
    current_password: str
    new_password: str


@router.post("/create", response_model=UserResponse)
async def create_user_endpoint(
    user_data: UserSchema,
    current_user: Users = Depends(get_current_user),
):
    """Create a new user in the system.

    Only admin users can create new users.

    Args:
        user_data: The user information required for creation.
        current_user: The currently authenticated user.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If user creation fails, validation error occurs, or user lacks permission.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin users can create new users",
        )

    try:
        user = await create_user_db(
            username=user_data.username,
            password=user_data.password,
            role=user_data.role,
        )
        return UserResponse(username=user.username, role=user.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: Users = Depends(get_current_user)):
    """Get all users in the system.

    Only admin users can view all users.

    Args:
        current_user: The currently authenticated user.

    Returns:
        List[UserResponse]: List of all users.

    Raises:
        HTTPException: If there's an error retrieving users or user lacks permission.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin users can view all users",
        )

    try:
        users = await get_all_users()
        return [UserResponse(username=user.username, role=user.role) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/get_api_key")
async def get_api_key(current_user: Users = Depends(get_current_user)):
    """Get API key of the currently authenticated user.

    Args:
        current_user: The currently authenticated user from JWT.

    Returns:
        JSON response with API key.
    """
    return {"api_key": current_user.api_key}


@router.post("/update_api_key")
async def update_user_api_key(current_user: Users = Depends(get_current_user)):
    """Update API key of the currently authenticated user.

    Args:
        current_user: The currently authenticated user from JWT.

    Returns:
        JSON response with new API key.

    Raises:
        HTTPException: If update fails.
    """
    async with async_session_maker() as session:
        # Get fresh user object in current session
        result = await session.execute(
            select(Users).where(Users.username == current_user.username)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        # Update API key
        user.api_key = str(uuid.uuid4().hex)
        await session.commit()
        return {"api_key": user.api_key}


@router.get("/usage")
async def get_usage(
    current_user: Users = Depends(get_current_user),
    username: str | None = None,
):
    """Get model usage statistics for a user.

    Basic users can only view their own usage.
    Admin users can view any user's usage.

    Args:
        current_user: The currently authenticated user.
        username: Optional username to fetch usage for (admin only).

    Returns:
        dict: A dictionary containing user's model usage statistics.

    Raises:
        HTTPException: If user is not found or other errors occur.
    """
    try:
        target_username = username if username else current_user.username
        
        if current_user.role != "admin" and target_username != current_user.username:
            raise HTTPException(
                status_code=403,
                detail="Basic users can only view their own usage",
            )

        usage = await get_usage_by_user_name(target_username)
        return usage
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/delete/{username}")
async def delete_user_endpoint(
    username: str,
    current_user: Users = Depends(get_current_user),
):
    """Delete a user from the system.

    Only admin users can delete users.

    Args:
        username: The username of the user to delete.
        current_user: The currently authenticated user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If user deletion fails or user lacks permission.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin users can delete users",
        )

    if username == current_user.username:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account",
        )

    success = await delete_user(username)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"User '{username}' not found",
        )

    return {"message": f"User '{username}' successfully deleted"}


@router.post("/set_usage_limit", deprecated=True)
async def set_user_usage_limit(
    request: UsageLimitRequest,
    current_user: Users = Depends(get_current_user),
):
    """Set usage limit for a user.

    Only admin users can set usage limits.

    Args:
        request: Request containing username and new limit.
        current_user: The currently authenticated user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If setting limit fails or user lacks permission.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin users can set usage limits",
        )

    success = await set_usage_limit(request.username, request.limit)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"User '{request.username}' not found",
        )

    return {
        "message": f"Usage limit for user '{request.username}' set to {request.limit}"
    }


@router.post("/update_password")
async def update_user_password(
    request: UpdatePasswordRequest,
    current_user: Users = Depends(get_current_user),
):
    """Update password of the currently authenticated user.

    Args:
        request: Request containing current and new passwords.
        current_user: The currently authenticated user from JWT.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If password update fails or verification fails.
    """
    success = await update_password(
        username=current_user.username,
        current_password=request.current_password,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=401,
            detail="현재 비밀번호가 일치하지 않습니다",
        )

    return {"message": "비밀번호가 성공적으로 변경되었습니다"}
