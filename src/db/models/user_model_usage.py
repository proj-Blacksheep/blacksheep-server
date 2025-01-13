"""User model usage module.

This module defines the database model for tracking user usage of AI models.
"""

from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.types import Enum as SQLAlchemyEnum

from src.db.models.base import Base, TimeStampMixin


class ModelUsageType(str, Enum):
    """Enum for the type of model usage."""

    COMPLETION = "COMPLETION"
    PROMPT = "PROMPT"
    CACHED = "CACHED"


class UserModelUsage(Base, TimeStampMixin):
    """Model for tracking user usage of AI models.

    Attributes:
        id: The unique identifier for the usage record.
        user_id: The ID of the user using the model.
        model_id: The ID of the used model.
        usage_type: The type of usage (e.g., inference, training).
        usage_count: The number of times the model was used.
    """

    __tablename__ = "user_model_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    usage_type = Column(SQLAlchemyEnum(ModelUsageType), nullable=False)
    usage_count = Column(Integer, default=0, nullable=False)
