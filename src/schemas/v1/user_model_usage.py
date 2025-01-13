"""User model usage schemas."""

from pydantic import BaseModel


class UserModelUsageDTO(BaseModel):
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
