"""User model usage service module.

This module provides functions for tracking and managing user model usage.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, update

from src.core.database import get_session
from src.db.models.user_model_usage import ModelUsageType, UserModelUsage
from src.db.models.users import UserORM


async def record_model_usage(
    user_id: int, model_id: int, usage_count: int, usage_type: ModelUsageType
) -> None:
    """Record model usage for a user.

    Args:
        user_id: The ID of the user.
        model_id: The ID of the model.
        usage_type: The type of usage (e.g., inference, training).
        usage_count: The number of times the model was used.
    """
    async with get_session() as session:
        # 기존 사용량 기록 조회
        result = await session.execute(
            select(UserModelUsage).where(
                UserModelUsage.user_id == user_id,
                UserModelUsage.model_id == model_id,
                UserModelUsage.usage_type == usage_type.value,
            )
        )
        usage_record = result.scalar_one_or_none()

        try:
            if usage_record:
                # 기존 기록이 있으면 업데이트
                await session.execute(
                    update(UserModelUsage)
                    .where(
                        UserModelUsage.user_id == user_id,
                        UserModelUsage.model_id == model_id,
                        UserModelUsage.usage_type == usage_type.value,
                    )
                    .values(usage_count=UserModelUsage.usage_count + usage_count)
                )
            else:
                # 새로운 기록 생성
                new_usage = UserModelUsage(
                    user_id=user_id,
                    model_id=model_id,
                    usage_type=usage_type.value,
                    usage_count=usage_count,
                )
                session.add(new_usage)

            await session.commit()
        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to record model usage: {str(e)}") from e


async def get_usage_by_user_name_and_date_range(
    username: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> dict[ModelUsageType, int]:
    """Get usage count for a user across all models within a date range.

    Args:
        username: The username to get usage for.
        start_date: Optional start date for filtering usage records.
        end_date: Optional end date for filtering usage records.

    Returns:
        dict[ModelUsageType, int]: Dictionary containing usage counts for each
            ModelUsageType. If there are no records for a specific type, it will
            have a value of 0.
    """
    async with get_session() as session:
        query = (
            select(UserModelUsage.usage_type, UserModelUsage.usage_count)
            .join(UserORM, UserModelUsage.user_id == UserORM.id)
            .where(UserORM.username == username)
        )

        if start_date:
            query = query.where(UserModelUsage.created_at >= start_date)
        if end_date:
            query = query.where(UserModelUsage.created_at <= end_date)

        result = await session.execute(query)

        # Initialize dictionary with 0 for all usage types
        usage_by_type = {usage_type: 0 for usage_type in ModelUsageType}

        # Sum up usage counts for each type
        for usage_type, count in result:
            usage_by_type[ModelUsageType(usage_type)] += count

        return usage_by_type


async def get_usage_by_user_name(username: str) -> dict[ModelUsageType, int]:
    """Get usage count for a user across all models, grouped by usage type.

    This function is maintained for backward compatibility.
    For more detailed queries, use get_usage_by_user_name_and_date_range.

    Args:
        username: The username to get usage for.

    Returns:
        dict[ModelUsageType, int]: Dictionary containing usage counts for each
            ModelUsageType. If there are no records for a specific type, it will
            have a value of 0.
    """
    return await get_usage_by_user_name_and_date_range(username)
