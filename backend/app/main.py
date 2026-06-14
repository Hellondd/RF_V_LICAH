from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as api_router
from app.config import settings
from app.database import engine, Base
from app.core.logging import setup_logging

# Создаём таблицы (пока пустые, но база будет готова)
Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI(title="Russia v Licah API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Russia v Licah API — skeleton ready. See /api/v1/health"}