from sqlalchemy import Column, Integer, String
from src.db.database import Base
from src.models.base import TimeStampMixin


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