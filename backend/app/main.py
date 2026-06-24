from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi import HTTPException
from app.api.v1 import router as api_router
from app.config import settings
from app.database import engine, Base
from app.core.logging import setup_logging
import app.models  # noqa: F401
from pathlib import Path


# Создаём таблицы (если их нет)
# Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI(title="Russia v Licah API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip сжатие для всех ответов больше 500 байт
app.add_middleware(GZipMiddleware, minimum_size=500)

# Подключаем API
app.include_router(api_router)

# ============================================================
# НАСТРОЙКА СТАТИКИ (ВАЖНО: конкретные папки ДО универсального маршрута!)
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = BASE_DIR / "uploads"

# Создаём папки, если их нет
UPLOADS_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "images").mkdir(exist_ok=True)

print(f"📁 FRONTEND_DIR: {FRONTEND_DIR} (exists: {FRONTEND_DIR.exists()})")

# ============================================================
# 1. СНАЧАЛА монтируем конкретные папки (css, js, images)
# ============================================================

if FRONTEND_DIR.exists():
    # CSS
    css_dir = FRONTEND_DIR / "css"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
        print("✅ CSS смонтирован по /css")
    else:
        print("⚠️ CSS папка не найдена")
    
    # JS
    js_dir = FRONTEND_DIR / "js"
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
        print("✅ JS смонтирован по /js")
    else:
        print("⚠️ JS папка не найдена")
    
    # Images из frontend
    frontend_images_dir = FRONTEND_DIR / "images"
    if frontend_images_dir.exists():
        app.mount("/images", StaticFiles(directory=str(frontend_images_dir)), name="images")
        print("✅ Images (frontend) смонтирован по /images")
    else:
        print("⚠️ Images папка в frontend не найдена")

# Монтируем uploads
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Монтируем static (если есть)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    print("✅ Static смонтирован по /static")

# ============================================================
# 2. ПОТОМ монтируем frontend (для HTML)
# ============================================================

if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")
    print("✅ Frontend смонтирован по /frontend")

# ============================================================
# ОСНОВНЫЕ МАРШРУТЫ (без универсального перехвата)
# ============================================================

@app.get("/")
async def root():
    """Главная страница"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Russia v Licah API", "docs": "/docs"}


@app.get("/index.html")
async def index_page():
    """Страница index.html (прямой доступ)"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    raise HTTPException(status_code=404, detail="index.html не найден")


@app.get("/regions.html")
async def regions_page():
    """Страница регионов"""
    html_path = FRONTEND_DIR / "regions.html"
    if html_path.exists():
        return FileResponse(str(html_path))
    raise HTTPException(status_code=404, detail="regions.html не найден")


@app.get("/{page}.html")
async def serve_html(page: str):
    """Динамическая раздача HTML страниц"""
    html_path = FRONTEND_DIR / f"{page}.html"
    if html_path.exists():
        return FileResponse(str(html_path))
    raise HTTPException(status_code=404, detail=f"Страница {page}.html не найдена")


# ============================================================
# ОБРАБОТЧИК 404
# ============================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Обработчик 404"""
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    
    # Пробуем вернуть index.html
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    
    return JSONResponse(status_code=404, content={"detail": "Not Found"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )