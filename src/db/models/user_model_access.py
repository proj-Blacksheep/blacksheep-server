"""User model access module.

This module defines the database model for tracking user access to AI models.
"""

from sqlalchemy import Column, ForeignKey, Integer, String

from src.db.models.base import Base, TimeStampMixin


class UserModelAccess(Base, TimeStampMixin):  # type: ignore
    """Model for tracking user access to AI models.

    Attributes:
        id: The unique identifier for the access record.
        user_id: The ID of the user accessing the model.
        model_id: The ID of the accessed model.
        access_type: The type of access (e.g., read, write).
    """

    __tablename__ = "user_model_access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    access_type = Column(String(50), nullable=False)
