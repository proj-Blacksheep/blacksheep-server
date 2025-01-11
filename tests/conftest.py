"""Pytest configuration and fixtures for all tests.

This module contains pytest fixtures that can be used across all tests.
This module is automatically loaded by pytest and fixtures defined here
are available to all test files.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session.

    This fixture provides a new event loop for the test session.

    Returns:
        Generator[asyncio.AbstractEventLoop, None, None]: Event loop instance
            that will be used for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_client() -> Generator[TestClient, None, None]:
    """Create a TestClient instance for synchronous API testing.

    This fixture provides a FastAPI TestClient for making synchronous HTTP requests
    during testing.

    Returns:
        Generator[TestClient, None, None]: TestClient instance that can be
            used for making synchronous requests to the FastAPI application.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def async_client(test_client: TestClient) -> AsyncGenerator[AsyncClient, None]:
    """Create an AsyncClient instance for asynchronous API testing.

    This fixture provides an HTTPX AsyncClient for making asynchronous HTTP requests
    during testing.

    Args:
        test_client: The synchronous TestClient fixture to get the base URL from.

    Returns:
        AsyncGenerator[AsyncClient, None]: AsyncClient instance that can be
            used for making asynchronous requests to the FastAPI application.
    """
    base_url = str(test_client.base_url)
    async with AsyncClient(base_url=base_url) as client:
        yield client
