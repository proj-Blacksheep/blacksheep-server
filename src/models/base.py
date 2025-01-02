from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from src.db.database import Base


class TimeStampMixin:
    """
    Adds created_at and updated_at columns to a table.
    """

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
