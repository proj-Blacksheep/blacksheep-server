from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.users import UserResponse
from src.services.users import create_user_db, get_all_users
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    """Request model for user creation.

    Attributes:
        username: The username for the new user.
        email: The email address of the user.
        password: The password for the user account.
    """

    username: str
    password: str


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
        raise HTTPException(status_code=400, detail=str(e))


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
        raise HTTPException(status_code=500, detail=str(e))
