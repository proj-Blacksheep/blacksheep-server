from sqlalchemy import Column, Integer, String
from src.db.database import Base
from src.models.base import TimeStampMixin


class Users(Base, TimeStampMixin):
    """
    User model for storing user related details.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    api_key = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(255), nullable=False)
