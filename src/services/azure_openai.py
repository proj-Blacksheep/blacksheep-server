"""Azure OpenAI service module.

This module provides functions for interacting with Azure OpenAI services.
"""

from typing import Optional, cast

import openai


async def call_azure_openai(
    model_name: str,
    prompt: str,
    max_tokens: Optional[int] = 100,
    temperature: Optional[float] = 0.7,
) -> str:
    """Call Azure OpenAI API.

    Args:
        model_name: The name of the model to use.
        prompt: The prompt to send to the model.
        max_tokens: Maximum number of tokens to generate.
        temperature: Sampling temperature to use.

    Returns:
        str: The model's response text.

    Raises:
        Exception: If the API call fails.
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return cast(str, response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Failed to call Azure OpenAI API: {str(e)}") from e
