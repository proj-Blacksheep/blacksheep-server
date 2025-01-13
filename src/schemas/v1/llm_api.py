"""API call request model."""

from typing import Optional

from pydantic import BaseModel


class APICallRequest(BaseModel):
    """API call request model.

    Attributes:
        model_name: The name of the model to call.
        prompt: The prompt to send to the model.
        max_tokens: Maximum number of tokens to generate.
        temperature: Sampling temperature to use.
    """

    model_name: str
    user_api_key: str
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
