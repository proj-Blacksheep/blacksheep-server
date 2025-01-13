"""Azure OpenAI service module.

This module provides functions for interacting with Azure OpenAI services.
"""

from typing import Optional, cast

from openai import AsyncAzureOpenAI

from src.core.utils import get_logger
from src.db.models.user_model_usage import ModelUsageType
from src.schemas.v1.models import ModelDTO
from src.services.user_model_usage import record_model_usage

logger = get_logger()


async def call_azure_openai(
    model: ModelDTO,
    prompt: str,
    api_version: str = "2024-10-01-preview",
    max_tokens: Optional[int] = 100,
    temperature: Optional[float] = 0.7,
    user_id: Optional[int] = None,
    model_id: Optional[int] = None,
) -> str:
    """Call Azure OpenAI API.

    Args:
        model: The model to use.
        prompt: The prompt to send to the model.
        max_tokens: Maximum number of tokens to generate.
        temperature: Sampling temperature to use.
        user_id: The ID of the user making the request.
        model_id: The ID of the model being used.

    Returns:
        str: The model's response text.

    Raises:
        Exception: If the API call fails.
    """
    try:
        client = AsyncAzureOpenAI(
            api_key=model.model_api_key,
            azure_endpoint=model.model_endpoint,
            api_version=api_version,
        )
        response = await client.chat.completions.create(
            model=model.model_deployment_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        if response.usage:
            if (
                hasattr(response.usage, "prompt_tokens_details")
                and response.usage.prompt_tokens_details
                and hasattr(response.usage.prompt_tokens_details, "cached_tokens")
            ):
                logger.info(
                    "Cached tokens: %s",
                    response.usage.prompt_tokens_details.cached_tokens,
                )
                if user_id is not None and model_id is not None:
                    await record_model_usage(
                        user_id=user_id,
                        model_id=model_id,
                        usage_type=ModelUsageType.CACHED,
                        usage_count=response.usage.prompt_tokens_details.cached_tokens
                        or 0,
                    )
            logger.info("Completion tokens: %s", response.usage.completion_tokens)
            logger.info("Prompt tokens: %s", response.usage.prompt_tokens)
            logger.info("Total tokens: %s", response.usage.total_tokens)

            # Record model usage if user_id and model_id are provided
            if user_id is not None and model_id is not None:
                await record_model_usage(
                    user_id=user_id,
                    model_id=model_id,
                    usage_type=ModelUsageType.COMPLETION,
                    usage_count=response.usage.completion_tokens,
                )

                await record_model_usage(
                    user_id=user_id,
                    model_id=model_id,
                    usage_type=ModelUsageType.PROMPT,
                    usage_count=response.usage.prompt_tokens,
                )

        return cast(str, response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Failed to call Azure OpenAI API: {str(e)}") from e
