from src.db.database import async_session_maker
from src.models.models import Models, ModelResponse
from sqlalchemy import select
from typing import List


async def create_model_db(
    name: str,
    description: str,
    model_endpoint: str,
    model_name: str,
    model_api_key: str,
) -> Models:
    """Create a new model in the database.

    Args:
        name: The name for the new model.
        description: The description for the model.
        model_endpoint: The endpoint for the model.
        model_name: The name for the model.
        model_api_key: The API key for the model.

    Returns:
        Models: The created model object.
    """
    async with async_session_maker() as session:

        new_model = Models(
            name=name,
            description=description,
            model_endpoint=model_endpoint,
            model_name=model_name,
            model_api_key=model_api_key,
        )

        session.add(new_model)
        await session.commit()
        await session.refresh(new_model)

        return new_model


async def get_all_models() -> List[ModelResponse]:
    """Get all models from the database.

    Returns:
        List[ModelResponse]: List of all models in the database.
    """
    async with async_session_maker() as session:
        result = await session.execute(select(Models))
        models = result.scalars().all()
        return list(models)