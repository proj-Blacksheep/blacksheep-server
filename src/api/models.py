from typing import List
from fastapi import APIRouter, HTTPException
from src.models.models import ModelResponse, ModelCreateRequest
from src.services.models import create_model_db, get_all_models

router = APIRouter(prefix="/models", tags=["models"])


@router.post("/create", response_model=ModelResponse)
async def create_model(model_data: ModelCreateRequest):
    """Create a new user in the system.

    Args:
        user_data: The user information required for creation.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If user creation fails or validation error occurs.
    """

    try:
        model = await create_model_db(
            name=model_data.name,
            description=model_data.description,
            model_endpoint=model_data.model_endpoint,
            model_name=model_data.model_name,
            model_api_key=model_data.model_api_key,
        )
        return model
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[ModelResponse])
async def get_models():
    """Get all users in the system.

    Returns:
        List[UserResponse]: List of all users.

    Raises:
        HTTPException: If there's an error retrieving users.
    """
    try:
        models = await get_all_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
