"""Health check endpoint tests.

This module contains tests for verifying the health check endpoint functionality.
These tests ensure that the API server is running and responding correctly.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


def test_health_check_sync(test_client: TestClient) -> None:
    """Test the health check endpoint using synchronous client.

    This test verifies that the health check endpoint returns a 200 status code
    and the expected response format using synchronous HTTP requests.

    Args:
        test_client: TestClient fixture for making synchronous requests.
    """
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_health_check_async(async_client: AsyncClient) -> None:
    """Test the health check endpoint using asynchronous client.

    This test verifies that the health check endpoint returns a 200 status code
    and the expected response format using asynchronous HTTP requests.

    Args:
        async_client: AsyncClient fixture for making asynchronous requests.
    """
    async for client in async_client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        break
