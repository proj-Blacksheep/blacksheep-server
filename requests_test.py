import requests
import json


def call_api():
    """Makes a POST request to the local API endpoint.

    Returns:
        dict: The JSON response from the API

    Raises:
        requests.RequestException: If the API request fails
    """
    url = "http://127.0.0.1:8000/api/"

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "model_name": "gpt4o-s",
        "user_api_key": "66d98be2d6c34d9990c6d291678ff9b2",
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
        return response.json()
    except requests.RequestException as e:
        print(f"API 호출 중 오류가 발생했습니다: {e}")
        raise


if __name__ == "__main__":
    try:
        result = call_api()
        print(json.loads(result))
    except Exception as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {e}")
