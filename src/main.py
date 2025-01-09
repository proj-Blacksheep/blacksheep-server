"""FastAPI application entry point.

This module initializes the FastAPI application, sets up CORS middleware,
includes routers, and provides health check endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import call_api, login, models, users
from src.core.config import settings
from src.db.database import init_db
from src.services.users import create_user_db

app = FastAPI(
    title="BlackSheep API",
    description="API for managing AI model access and usage",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(login.router)
app.include_router(users.router)
app.include_router(models.router)
app.include_router(call_api.router)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize database and other startup tasks.

    This function is called when the application starts up.
    It initializes the database by creating all necessary tables
    and creates a default admin user if it doesn't exist.
    """
    await init_db()

    # Create default admin user
    await create_user_db(
        username=settings.DEFAULT_ADMIN_USERNAME,
        password=settings.DEFAULT_ADMIN_PASSWORD,
        role="admin",
    )


@app.get("/")
async def root() -> dict:
    """Root endpoint for health check.

    Returns:
        dict: Basic health check response.
    """
    return {"status": "healthy", "message": "BlackSheep API is running"}


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: Detailed health check response.
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }
