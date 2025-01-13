"""SQLAlchemy models for user management."""

from sqlalchemy import Boolean, Column, Integer, String

from src.db.models.base import Base, TimeStampMixin


class UserORM(Base, TimeStampMixin):  # type: ignore
    """SQLAlchemy model for storing user related details.

    Attributes:
        id: The unique identifier for the user.
        username: The unique username for the user.
        password: The hashed password for the user.
        api_key: The unique API key for the user.
        is_admin: The role of the user (basic or admin).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    api_key = Column(String(255), unique=True, index=True, nullable=False)
    is_admin = Column(Boolean, default=False)
