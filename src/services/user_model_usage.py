from src.models.user_model_usage import UserModelUsage
from src.models.users import Users
from src.models.models import Models
from src.db.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def user_model_usage(
    user_name: int,
    model_name: int,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
):
    """Create a new user model usage record.

    Args:
        user_name: The ID of the user.
        model_name: The ID of the model.
        input_tokens: Number of input tokens used.
        output_tokens: Number of output tokens used.
        total_tokens: Total number of tokens used.

    Returns:
        UserModelUsage: The created user model usage record.
    """
    async with async_session_maker() as session:
        new_user_model_usage = UserModelUsage(
            user_id=user_name,
            model_id=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )

        session.add(new_user_model_usage)
        await session.commit()
        await session.refresh(new_user_model_usage)

        return new_user_model_usage


async def get_usage_by_user_name(username: str):
    """Get all model usage records for a specific user.

    Args:
        username: The username to fetch usage records for.

    Returns:
        dict: A dictionary containing user's model usage statistics.
        Format:
        {
            "total_usage": {
                "input_tokens": int,
                "output_tokens": int,
                "total_tokens": int
            },
            "model_usage": [
                {
                    "model_name": str,
                    "input_tokens": int,
                    "output_tokens": int,
                    "total_tokens": int
                },
                ...
            ]
        }

    Raises:
        ValueError: If the user is not found.
    """
    async with async_session_maker() as session:
        # Get user ID from username
        user_query = select(Users).where(Users.username == username)
        user_result = await session.execute(user_query)
        user = user_result.scalar_one_or_none()

        if not user:
            raise ValueError(f"사용자를 찾을 수 없습니다: {username}")

        # Get all usage records for the user
        usage_query = (
            select(UserModelUsage, Models)
            .join(Models, UserModelUsage.model_id == Models.id)
            .where(UserModelUsage.user_id == user.id)
        )

        usage_results = await session.execute(usage_query)
        usage_records = usage_results.all()

        # Initialize response structure
        response = {
            "total_usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
            "model_usage": [],
        }

        # Group usage by model
        model_usage_map = {}

        for usage, model in usage_records:
            # Update total usage
            response["total_usage"]["input_tokens"] += usage.input_tokens
            response["total_usage"]["output_tokens"] += usage.output_tokens
            response["total_usage"]["total_tokens"] += usage.total_tokens

            # Update or create model specific usage
            if model.name not in model_usage_map:
                model_usage_map[model.name] = {
                    "model_name": model.name,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                }

            model_usage_map[model.name]["input_tokens"] += usage.input_tokens
            model_usage_map[model.name]["output_tokens"] += usage.output_tokens
            model_usage_map[model.name]["total_tokens"] += usage.total_tokens

        response["model_usage"] = list(model_usage_map.values())
        return response
