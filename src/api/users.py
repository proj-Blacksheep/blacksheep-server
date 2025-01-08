from typing import List
from fastapi import APIRouter, HTTPException
from src.models.users import UserResponse, UserSchema
from src.services.users import create_user_db, get_all_users, get_api_key_by_credentials
from src.services.user_model_usage import get_usage_by_user_name
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])


class GetApiKeyRequest(BaseModel):
    username: str
    password: str


@router.post("/create", response_model=UserResponse)
async def create_user_endpoint(user_data: UserSchema):
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


@router.post("/get-api-key")
async def get_api_key(form_data: GetApiKeyRequest):
    """Get API key using username and password.

    Args:
        form_data: Request containing username and password

    Returns:
        JSON response with API key

    Raises:
        HTTPException: If credentials are invalid
    """
    api_key = await get_api_key_by_credentials(form_data.username, form_data.password)
    if not api_key:
        raise HTTPException(status_code=401, detail="유효하지 않은 인증 정보입니다.")

    return {"api_key": api_key}


@router.get("/usage")
async def get_usage(user_name: str):
    """Get model usage statistics for a specific user.

    Args:
        user_name: The username to fetch usage statistics for.

    Returns:
        dict: A dictionary containing user's model usage statistics.

    Raises:
        HTTPException: If user is not found or other errors occur.
    """
    try:
        usage = await get_usage_by_user_name(user_name)
        return usage
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
