"""API response models module.

This module defines Pydantic models for API responses and data validation,
as well as SQLAlchemy models for database tables.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
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


class ModelResponse(BaseModel):
    """Model response model.

    Attributes:
        model_name: The name of the model.
        model_type: The type of the model.
        created_at: The timestamp when the model was created.
    """

    model_name: str
    model_type: str
    created_at: Optional[datetime] = None


class UserCreate(BaseModel):
    """User creation request model.

    Attributes:
        username: The username for the new user.
        password: The password for the user account.
        role: The role of the user (basic or admin).
    """

    username: str
    password: str
    role: str = "basic"


class UserResponse(BaseModel):
    """User response model.

    Attributes:
        username: The username of the user.
        role: The role of the user (basic or admin).
        api_key: The API key for the user.
    """

    username: str
    role: str
    api_key: str


class Token(BaseModel):
    """Token response model.

    Attributes:
        access_token: The JWT access token.
        token_type: The type of token (e.g., 'bearer').
    """

    access_token: str
    token_type: str
