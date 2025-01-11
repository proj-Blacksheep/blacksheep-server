"""API call module.

This module provides endpoints for making API calls to external services.
"""

from typing import Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.services.azure_openai import call_azure_openai


class APICallRequest(BaseModel):
    """API call request model.

    Attributes:
        model_name: The name of the model to call.
        prompt: The prompt to send to the model.
        max_tokens: Maximum number of tokens to generate.
        temperature: Sampling temperature to use.
    """

    model_name: str
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7


router = APIRouter(prefix="/api", tags=["api"])


@router.post("/call", response_model=Dict[str, str])
async def call_api(request: APICallRequest) -> Dict[str, str]:
    """Make an API call to the specified model.

    Args:
        request: The API call request parameters.

    Returns:
        Dict[str, str]: The model's response.

    Raises:
        HTTPException: If the user is not authorized or the model call fails.
    """
    try:
        response = await call_azure_openai(
            request.model_name,
            request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
