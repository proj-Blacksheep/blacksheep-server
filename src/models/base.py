"""Base models and mixins for SQLAlchemy models."""

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimeStampMixin:
    """Mixin that adds created_at and updated_at timestamps to models."""

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
