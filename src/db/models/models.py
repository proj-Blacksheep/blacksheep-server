"""API response models module.

This module defines Pydantic models for API responses and data validation,
as well as SQLAlchemy models for database tables.
"""

from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String

from src.db.models.base import Base, TimeStampMixin


class ModelType(str, Enum):
    """Enum for the type of model."""

    AZURE_OPENAI = "AZURE_OPENAI"
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"
    GEMINI = "GEMINI"
    GCP_GEMINI = "GCP_GEMINI"


class Models(Base, TimeStampMixin):  # type: ignore
    """Model for storing AI model information.

    Attributes:
        id: The unique identifier for the model.
        model_name: The name of the model.
        model_type: The type of the model.
    """

    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), unique=True, index=True, nullable=False)
    model_type = Column(SQLAlchemyEnum(ModelType), nullable=False)
    model_description = Column(String(255), nullable=True)
    model_endpoint = Column(String(255), nullable=False)
    model_api_key = Column(String(255), nullable=False)
    model_deployment_name = Column(String(255), nullable=False)
