"""Model management service module.

This module provides functions for managing AI models in the database,
including creation, deletion, and retrieval operations.
"""

from typing import List, Optional

from sqlalchemy import delete, select

from src.db.database import get_session
from src.models.models import Models


async def create_model_db(
    model_name: str, model_type: str, model_endpoint: str, model_api_key: str
) -> Optional[Models]:
    """Create a new model in the database.

    Args:
        model_name: The name of the model.
        model_type: The type of the model.

    Returns:
        Optional[Models]: The created model object, or None if creation fails.
    """
    async with get_session() as session:
        # Check if model already exists
        result = await session.execute(
            select(Models).where(Models.model_name == model_name)
        )
        model = result.scalar_one_or_none()
        if model:
            return None

        new_model = Models(
            model_name=model_name,
            model_type=model_type,
        )
        session.add(new_model)
        await session.commit()
        await session.refresh(new_model)
        return new_model


async def get_all_models() -> List[Models]:
    """Get all models from the database.

    Returns:
        List[Models]: List of all models.
    """
    async with get_session() as session:
        result = await session.execute(select(Models))
        models = result.scalars().all()
        return list(models)


async def delete_model(model_name: str) -> bool:
    """Delete a model from the database.

    Args:
        model_name: The name of the model to delete.

    Returns:
        bool: True if model was deleted, False if model was not found.
    """
    async with get_session() as session:
        result = await session.execute(
            delete(Models).where(Models.model_name == model_name)
        )
        if result.rowcount > 0:
            await session.commit()
            return True
        return False
