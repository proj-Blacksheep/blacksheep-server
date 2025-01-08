from typing import List, Dict, Any, AsyncGenerator, cast
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import async_session_maker
from src.models.users import Users
from src.models.models import Models
from src.services.azure_openai import call_azure_openai
from typing import Optional

router = APIRouter(prefix="/api", tags=["api"])


class Message(BaseModel):
    role: str
    content: str


class CallApiRequest(BaseModel):
    """Request model for API calls.

    Attributes:
        model_name: Name of the model to use for inference
        user_api_key: API key for user authentication
        prompt: List of message dictionaries containing role and content
    """

    model_name: str
    user_api_key: str
    prompt: List[Dict[str, str]]
    response_format: Optional[Any] = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session.

    Returns:
        AsyncGenerator[AsyncSession, None]: Database session
    """
    async with async_session_maker() as session:
        yield session


async def get_user(api_key: str, db: AsyncSession) -> Users:
    """Get user by API key.

    Args:
        api_key: User's API key
        db: Database session

    Returns:
        Users: User object

    Raises:
        HTTPException: If user is not found
    """
    user = (
        await db.execute(select(Users).where(Users.api_key == api_key))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="유효하지 않은 API 키입니다.")
    return user


async def get_model(model_name: str, db: AsyncSession) -> Models:
    """Get model by name.

    Args:
        model_name: Name of the model
        db: Database session

    Returns:
        Models: Model object

    Raises:
        HTTPException: If model is not found
    """
    model = (
        await db.execute(select(Models).where(Models.name == model_name))
    ).scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="요청한 모델을 찾을 수 없습니다.")
    return model


@router.post("/")
async def call_api(
    form_data: CallApiRequest, db: AsyncSession = Depends(get_db)
) -> Any:
    """Process API call after validating user and model.

    Args:
        form_data: API request data containing user_api_key, model_name and prompt
        db: Database session

    Returns:
        Any: Response from the model

    Raises:
        HTTPException: If validation fails
    """
    user = await get_user(form_data.user_api_key, db)
    model = await get_model(form_data.model_name, db)

    response = await call_azure_openai(
        api_key=str(model.model_api_key),
        endpoint=str(model.model_endpoint),
        messages=form_data.prompt,
        model_name=str(model.model_name),
        user_id=cast(int, user.id),
        model_id=cast(int, model.id),
        db=db,
        response_format=form_data.response_format,
    )

    return response
