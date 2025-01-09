"""SQLAlchemy models for user management."""

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from src.db.database import Base
from src.models.base import TimeStampMixin


class Users(Base):
    """SQLAlchemy model for storing user related details.

    Attributes:
        id: The unique identifier for the user.
        username: The unique username for the user.
        password: The hashed password for the user.
        api_key: The unique API key for the user.
        role: The role of the user (basic or admin).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    api_key = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(255), nullable=False)

    created_at = TimeStampMixin.created_at
    updated_at = TimeStampMixin.updated_at


class UserResponse(BaseModel):
    """Pydantic model for user response.

    Attributes:
        username: The username of the user.
        role: The role of the user.
    """

    username: str
    role: str


class UserSchema(BaseModel):
    """Request model for user creation.

    Attributes:
        username: The username for the new user.
        password: The password for the user account.
        role: The role of the user (defaults to "basic").
    """

    username: str
    password: str
    role: str = "basic"
