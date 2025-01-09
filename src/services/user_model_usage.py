"""User model usage service module.

This module provides functions for managing user model usage records.
"""

from typing import Dict

from sqlalchemy import select

from src.db.database import get_session
from src.models.user_model_usage import UserModelUsage
from src.models.users import Users


async def get_usage_by_user_name(username: str) -> Dict[str, int]:
    """Get model usage statistics for a user.

    Args:
        username: The username to get usage for.

    Returns:
        Dict[str, int]: Dictionary containing usage statistics.
    """
    async with get_session() as session:
        # Get user ID
        result = await session.execute(select(Users).where(Users.username == username))
        user = result.scalar_one_or_none()
        if not user:
            return {}

        # Get usage records
        result = await session.execute(
            select(UserModelUsage).where(UserModelUsage.user_id == user.id)
        )
        usage_records = result.scalars().all()

        # Aggregate usage
        usage_stats = {
            "total_usage": sum(record.usage_count for record in usage_records),
            "by_type": {},
        }

        for record in usage_records:
            if record.usage_type not in usage_stats["by_type"]:
                usage_stats["by_type"][record.usage_type] = 0
            usage_stats["by_type"][record.usage_type] += record.usage_count

        return usage_stats


async def record_model_usage(
    username: str, model_id: int, usage_type: str, count: int = 1
) -> bool:
    """Record model usage for a user.

    Args:
        username: The username of the user.
        model_id: The ID of the model used.
        usage_type: The type of usage.
        count: The number of times the model was used.

    Returns:
        bool: True if usage was recorded successfully, False otherwise.
    """
    async with get_session() as session:
        # Get user ID
        result = await session.execute(select(Users).where(Users.username == username))
        user = result.scalar_one_or_none()
        if not user:
            return False

        # Create or update usage record
        result = await session.execute(
            select(UserModelUsage).where(
                UserModelUsage.user_id == user.id,
                UserModelUsage.model_id == model_id,
                UserModelUsage.usage_type == usage_type,
            )
        )
        usage_record = result.scalar_one_or_none()

        if usage_record:
            usage_record.usage_count += count
        else:
            usage_record = UserModelUsage(
                user_id=user.id,
                model_id=model_id,
                usage_type=usage_type,
                usage_count=count,
            )
            session.add(usage_record)

        await session.commit()
        return True
