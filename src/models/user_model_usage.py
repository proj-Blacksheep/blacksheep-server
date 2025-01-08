from sqlalchemy import Column, ForeignKey, Integer
from src.db.database import Base
from src.models.base import TimeStampMixin


class UserModelUsage(Base, TimeStampMixin):
    """
    User model for storing user related details.
    """

    __tablename__ = "user_model_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)
