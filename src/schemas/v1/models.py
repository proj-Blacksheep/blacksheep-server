"""Models schemas."""

from pydantic import BaseModel, Field

from src.db.models.models import ModelType


class ModelDTO(BaseModel):
    """Data Transfer Object for Model.

    Attributes:
        id: The unique identifier for the model.
        model_name: The name of the model.
        model_type: The type of the model.
    """

    id: int
    model_name: str
    model_type: str
    model_description: str
    model_endpoint: str
    model_api_key: str
    model_deployment_name: str

    class Config:
        """Pydantic model configuration."""

        from_attributes = True


class ModelCreateRequest(BaseModel):
    """Model create model.

    Attributes:
        model_name: The name of the model.
        model_type: The type of the model.
    """

    model_name: str = Field(..., description="The name of the model")
    model_type: ModelType = Field(..., description="The type of the model")
    model_deployment_name: str = Field(
        ..., description="The deployment name of the model"
    )
    model_description: str = Field(..., description="The description of the model")
    model_endpoint: str = Field(..., description="The endpoint of the model")
    model_api_key: str = Field(..., description="The API key of the model")
