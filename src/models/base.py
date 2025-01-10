"""Base model module for SQLAlchemy models."""

from sqlalchemy import Column, DateTime, text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


class TimeStampMixin:
    """Mixin for adding timestamp columns to a model."""

    created_at = Column(DateTime, server_default=text("NOW()"))
    updated_at = Column(DateTime, server_default=text("NOW()"), onupdate=text("NOW()"))
