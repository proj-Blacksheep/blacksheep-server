from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from src.db.database import Base
from src.models.base import TimeStampMixin


class Users(Base, TimeStampMixin):
    """SQLAlchemy model for storing user related details."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    api_key = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(255), nullable=False)


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
    """

    username: str
    password: str
    role: str = "basic"
