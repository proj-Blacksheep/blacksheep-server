"""Test module for making API requests to the local server.

This module provides functionality to test the API endpoints by making POST requests
with specific JSON payloads and handling the responses.
"""

from typing import Any, cast

import requests


def call_api() -> dict[str, Any]:
    """Makes a POST request to the local API endpoint.

    Returns:
        dict[str, Any]: The JSON response from the API

    Raises:
        requests.RequestException: If the API request fails
    """
    url = "http://127.0.0.1:8000/api/"

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "model_name": "gpt4o-s",
        "user_api_key": "this_is_test_api_key",
        "prompt": [
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {
                "role": "user",
                "content": "삶이란 무엇인지 간단한하게 표현해줘",
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "whats_the_life",
                "schema": {
                    "type": "object",
                    "properties": {
                        "life": {
                            "type": "string",
                            "description": "life",
                        },
                        "reason": {
                            "type": "string",
                            "description": "reason",
                        },
                    },
                    "required": ["life", "reason"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 에러 발생 시 예외를 발생시킵니다
        return cast(dict[str, Any], response.json())
    except requests.RequestException as e:
        print(f"API 호출 중 오류가 발생했습니다: {e}")
        raise


if __name__ == "__main__":
    try:
        result = call_api()
        print(result)  # result는 이미 dictionary이므로 json.loads() 불필요
    except Exception as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {e}")
