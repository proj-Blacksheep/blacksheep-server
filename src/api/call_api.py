from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from src.db.database import async_session_maker
from src.models.users import Users
from src.models.models import Models
from src.services.azure_openai import call_azure_openai

router = APIRouter(prefix="/api", tags=["api"])


class CallApiRequest(BaseModel):
    model_name: str
    user_api_key: str
    prompt: List[Dict]


@router.post("/")
async def call_api(form_data: CallApiRequest):
    """Validate user API key and model, then process the API call.

    Args:
        form_data: API request data containing user_api_key, model_name and prompt

    Returns:
        JSON response with success message

    Raises:
        HTTPException: If API key is invalid, user not found, or model not found
    """
    async with async_session_maker() as session:
        # 사용자 검증
        user_result = await session.execute(
            select(Users).where(Users.api_key == form_data.user_api_key)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="유효하지 않은 API 키입니다.")

        # 모델 검증
        model_result = await session.execute(
            select(Models).where(Models.name == form_data.model_name)
        )
        model = model_result.scalar_one_or_none()

        if not model:
            raise HTTPException(
                status_code=404, detail="요청한 모델을 찾을 수 없습니다."
            )

        response = await call_azure_openai(
            api_key=str(model.model_api_key),
            endpoint=str(model.model_endpoint),
            messages=form_data.prompt,
            model_name=str(model.model_name),
            user_id=getattr(user, "id"),
            model_id=getattr(model, "id"),
            db=session,
        )

        return response
