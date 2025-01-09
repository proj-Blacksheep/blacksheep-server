from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.models import ModelResponse, ModelCreateRequest
from src.services.models import create_model_db, get_all_models, delete_model_db
from src.core.authentication import get_current_user

router = APIRouter(prefix="/models", tags=["models"])


@router.post("/create", response_model=ModelResponse)
async def create_model(
    model_data: ModelCreateRequest, current_user=Depends(get_current_user)
):
    """Create a new model in the system.

    Args:
        model_data: The model information required for creation.
        current_user: The authenticated user making the request.

    Returns:
        ModelResponse: The created model object.

    Raises:
        HTTPException: If model creation fails, validation error occurs, or user is not authenticated.
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
async def get_models(current_user=Depends(get_current_user)):
    """Get all models in the system.

    Returns:
        List[ModelResponse]: List of all models.

    Raises:
        HTTPException: If there's an error retrieving models.
    """
    try:
        models = await get_all_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{model_name}", response_model=bool)
async def delete_model(model_name: str, current_user=Depends(get_current_user)):
    """Delete a model from the system.

    Args:
        model_name: The name of the model to delete.
        current_user: The authenticated user making the request.

    Returns:
        bool: True if deletion was successful.

    Raises:
        HTTPException: If model deletion fails or model is not found.
    """
    try:
        result = await delete_model_db(model_name)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
