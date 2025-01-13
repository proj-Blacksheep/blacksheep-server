"""API call module.

This module provides endpoints for making API calls to external services.
"""

from typing import Dict

from fastapi import APIRouter, HTTPException, status

from src.core.utils import get_logger
from src.db.models.models import ModelType
from src.schemas.v1.llm_api import APICallRequest
from src.services.azure_openai import call_azure_openai
from src.services.models import get_model_by_name
from src.services.users import UserService

logger = get_logger()
user_service = UserService()

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/call", response_model=Dict[str, str])
async def call_api(request: APICallRequest) -> Dict[str, str]:
    """Make an API call to the specified model.

    Args:
        request: The API call request parameters.

    Returns:
        Dict[str, str]: The model's response.

    Raises:
        HTTPException: If the user is not authorized, model not found,
            or the model call fails.
    """
    try:
        user = await user_service.get_user_by_api_key(request.user_api_key)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )

        model = await get_model_by_name(request.model_name)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model {request.model_name} not found",
            )

        match model.model_type:
            case ModelType.AZURE_OPENAI.value:
                response = await call_azure_openai(
                    model,
                    request.prompt,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    user_id=user.id,
                    model_id=model.id,
                )
                return {"response": response}
            case _:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported model type: {model.model_type}",
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
