from sqlalchemy import Column, ForeignKey, Integer, String
from src.db.database import Base
from src.models.base import TimeStampMixin


class UserModelAccess(Base, TimeStampMixin):
    """
    User model for storing user related details.
    """

    __tablename__ = "user_model_access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    access_level = Column(String(255), nullable=False)
