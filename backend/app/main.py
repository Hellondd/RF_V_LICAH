from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as api_router
from app.config import settings
from app.database import engine, Base
from app.core.logging import setup_logging
import app.models  # noqa: F401


# Создаём таблицы (если их нет) — но мы уже отключили, оставим на всякий случай
# Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI(title="Russia v Licah API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API
app.include_router(api_router)

# Монтируем папку frontend как статику
app.mount("/", StaticFiles(directory="/frontend", html=True), name="frontend")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/images", StaticFiles(directory="static/images"), name="images")

# Дополнительный корневой эндпоинт на случай, если статика не сработает
@app.get("/")
def root():
    from fastapi.responses import FileResponse
    return FileResponse("frontend/index.html")