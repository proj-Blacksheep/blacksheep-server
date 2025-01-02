from typing import List
from fastapi import APIRouter, HTTPException
from src.models.users import UserResponse, UserCreate
from src.services.users import create_user_db, get_all_users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_model=UserResponse)
async def create_user_endpoint(user_data: UserCreate):
    """Create a new user in the system.

    Args:
        user_data: The user information required for creation.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If user creation fails or validation error occurs.
    """

    try:
        user = await create_user_db(
            username=user_data.username, password=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[UserResponse])
async def get_users():
    """Get all users in the system.

    Returns:
        List[UserResponse]: List of all users.

    Raises:
        HTTPException: If there's an error retrieving users.
    """
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


