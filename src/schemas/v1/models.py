"""Models schemas."""

from pydantic import BaseModel, Field


class ModelCreateRequest(BaseModel):
    """Model create model.

    Attributes:
        model_name: The name of the model.
        model_type: The type of the model.
    """

    model_name: str = Field(..., description="The name of the model")
    model_type: str = Field(..., description="The type of the model")
    model_endpoint: str = Field(..., description="The endpoint of the model")
    model_api_key: str = Field(..., description="The API key of the model")
