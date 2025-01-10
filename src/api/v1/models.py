"""Model API endpoints module.

This module provides API endpoints for model management operations including
model creation, deletion, and updates.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.authentication import get_current_user
from src.schemas.v1.models import ModelCreateRequest
from src.schemas.v1.users import UserDTO
from src.services.models import create_model_db, delete_model, get_all_models

router = APIRouter(
    prefix="/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_model(
    model: ModelCreateRequest,
    current_user: UserDTO = Depends(get_current_user),
) -> Dict[str, str]:
    """Create a new model.

    Args:
        model: ModelCreateRequest.
        current_user: Current authenticated user.

    Returns:
        Dict[str, str]: Success message with model name.

    Raises:
        HTTPException: If model creation fails or user is not authorized.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    model = await create_model_db(
        model_name=model.model_name,
        model_type=model.model_type,
        model_endpoint=model.model_endpoint,
        model_api_key=model.model_api_key,
    )
    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create model",
        )

    return {"message": f"Model {model.model_name} created successfully"}


@router.get("/all")
async def get_models(
    _: UserDTO = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """Get all models.

    Args:
        current_user: Current authenticated user.

    Returns:
        List[Dict[str, Any]]: List of all models information.

    Raises:
        HTTPException: If user is not authorized.
    """
    models = await get_all_models()
    return [
        {
            "model_name": model.model_name,
            "model_type": model.model_type,
            "created_at": model.created_at,
        }
        for model in models
    ]


@router.delete("/{model_name}")
async def remove_model(
    model_name: str,
    current_user: UserDTO = Depends(get_current_user),
) -> Dict[str, str]:
    """Delete a model.

    Args:
        model_name: Name of the model to delete.
        current_user: Current authenticated user.

    Returns:
        Dict[str, str]: Success message.

    Raises:
        HTTPException: If model deletion fails or user is not authorized.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    success = await delete_model(model_name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )

    return {"message": f"Model {model_name} deleted successfully"}
