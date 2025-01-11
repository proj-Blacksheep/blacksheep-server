"""User model usage service module.

This module provides functions for managing user model usage records.
"""

from typing import Dict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.di import get_db, get_user_model_usage_repository, get_user_repository
from src.repositories.user_model_usage import UserModelUsageRepository
from src.repositories.users import UserRepository


async def get_usage_by_user_name(
    username: str,
    db: AsyncSession = Depends(get_db),
    user_repository: UserRepository = Depends(get_user_repository),
    usage_repository: UserModelUsageRepository = Depends(
        get_user_model_usage_repository
    ),
) -> Dict[str, int]:
    """Get model usage statistics for a user.

    Args:
        username: The username to get usage for.
        db: Database session.
        user_repository: User repository instance.
        usage_repository: User model usage repository instance.

    Returns:
        Dict[str, int]: Dictionary containing usage statistics.
    """
    user = await user_repository.get_by_username(db, username)
    if user is None:
        return {}

    usage_records = await usage_repository.get_by_user_id(db, int(user.id))

    # Aggregate usage
    usage_stats = {
        "total_usage": sum(int(record.usage_count) for record in usage_records),
        "by_type": {},
    }

    for record in usage_records:
        usage_type = str(record.usage_type)
        if usage_type not in usage_stats["by_type"]:
            usage_stats["by_type"][usage_type] = 0
        usage_stats["by_type"][usage_type] += int(record.usage_count)

    return usage_stats


async def record_model_usage(
    username: str,
    model_id: int,
    usage_type: str,
    count: int = 1,
    db: AsyncSession = Depends(get_db),
    user_repository: UserRepository = Depends(get_user_repository),
    usage_repository: UserModelUsageRepository = Depends(
        get_user_model_usage_repository
    ),
) -> bool:
    """Record model usage for a user.

    Args:
        username: The username of the user.
        model_id: The ID of the model used.
        usage_type: The type of usage.
        count: The number of times the model was used.
        db: Database session.
        user_repository: User repository instance.
        usage_repository: User model usage repository instance.

    Returns:
        bool: True if usage was recorded successfully, False otherwise.
    """
    user = await user_repository.get_by_username(db, username)
    if user is None:
        return False

    await usage_repository.create_or_update(
        db,
        user_id=int(user.id),
        model_id=model_id,
        usage_type=usage_type,
        count=count,
    )
    return True
