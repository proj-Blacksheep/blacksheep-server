from openai import AsyncAzureOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_model_usage import UserModelUsage
from typing import Optional, Any


async def call_azure_openai(
    api_key: str,
    endpoint: str,
    messages: list,
    model_name: str,
    user_id: int,
    model_id: int,
    db: AsyncSession,
    response_format: Optional[Any] = None,
) -> str:
    """Creates an async Azure OpenAI client, makes API calls and saves token usage.

    Args:
        api_key: The API key for the Azure OpenAI API.
        endpoint: The endpoint for the Azure OpenAI API.
        messages: The messages to send to the Azure OpenAI API.
        model_name: The name of the model to use for the Azure OpenAI API call.
        user_id: The ID of the user making the request.
        model_id: The ID of the model being used.
        db: The database session.

    Returns:
        The response content from the Azure OpenAI API call.
    """
    azure_openai_client = AsyncAzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version="2024-10-01-preview",
    )

    if response_format is not None:
        response = await azure_openai_client.chat.completions.create(
            messages=messages,
            model=model_name,
            response_format=response_format,
        )
    else:
        response = await azure_openai_client.chat.completions.create(
            messages=messages,
            model=model_name,
        )

    response_content = response.choices[0].message.content
    print(response_content)
    if response_content is None:
        raise ValueError("No response content received from Azure OpenAI API")

    # Clean response content if it's wrapped in JSON
    if response_content.startswith("```") and response_content.endswith("```"):
        response_content = response_content[3:-3]
        if response_content.startswith("json\n"):
            response_content = response_content[5:]

    input_tokens = getattr(response.usage, "prompt_tokens", 0)
    output_tokens = getattr(response.usage, "completion_tokens", 0)
    total_tokens = getattr(response.usage, "total_tokens", 0)

    # Save token usage to database
    usage = UserModelUsage(
        user_id=user_id,
        model_id=model_id,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )
    db.add(usage)
    await db.commit()

    return response_content
