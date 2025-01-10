"""API response models module.

This module defines Pydantic models for API responses and data validation,
as well as SQLAlchemy models for database tables.
"""

from sqlalchemy import Column, Integer, String

from src.db.database import Base
from src.models.base import TimeStampMixin


class Models(Base, TimeStampMixin):
    """Model for storing AI model information.

    Attributes:
        id: The unique identifier for the model.
        model_name: The name of the model.
        model_type: The type of the model.
    """

    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), unique=True, index=True, nullable=False)
    model_type = Column(String(255), nullable=False)
    model_endpoint = Column(String(255), nullable=False)
    model_api_key = Column(String(255), nullable=False)
