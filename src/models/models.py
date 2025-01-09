from sqlalchemy import Column, Integer, String
from src.db.database import Base
from src.models.base import TimeStampMixin
from pydantic import BaseModel


class Models(Base, TimeStampMixin):
    """
    User model for storing user related details.
    """

    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=False)
    model_api_key = Column(String(255), unique=True, index=True, nullable=False)
    model_endpoint = Column(String(255), nullable=False)
    model_name = Column(String(255), nullable=False)


class ModelResponse(BaseModel):
    id: int
    name: str
    description: str
    model_endpoint: str
    model_name: str


class ModelCreateRequest(BaseModel):
    name: str
    description: str
    model_endpoint: str
    model_api_key: str
    model_name: str


class UserResponse(BaseModel):
    """Response model for user data.

    Attributes:
        id: The user's unique identifier.
        username: The user's username.
        email: The user's email address.
        role: The user's role in the system.
    """

    id: int
    username: str
    role: str
