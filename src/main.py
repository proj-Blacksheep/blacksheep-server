from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import init_db

app = FastAPI(
    title="FastAPI Template", description="FastAPI 프로젝트 템플릿", version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행되는 이벤트"""
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
