from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import init_db
from src.api.users import router as users_router
from src.api.login import router as login_router
from src.core.config import settings
from src.services.users import create_user_db
from sqlalchemy.exc import IntegrityError
from src.api.models import router as models_router
from src.api.call_api import router as call_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.

    This context manager handles database initialization and creates a default admin user
    if one doesn't exist.

    Args:
        app: The FastAPI application instance.
    """
    await init_db()

    try:
        await create_user_db(
            username=settings.DEFAULT_ADMIN_USERNAME,
            password=settings.DEFAULT_ADMIN_PASSWORD,
            role="admin",
        )
    except IntegrityError:
        pass

    yield


app = FastAPI(
    title="FastAPI Template",
    description="FastAPI 프로젝트 템플릿",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "users", "description": "User management operations"},
        {"name": "login", "description": "Authentication operations"},
        {"name": "models", "description": "Model management operations"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "OK"}


app.include_router(users_router)
app.include_router(login_router)
app.include_router(models_router)
app.include_router(call_api_router)
