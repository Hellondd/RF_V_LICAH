from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(tags=["ping"])

@router.get("/ping")
async def ping_db(db: Session = Depends(get_db)):
    # Простейший запрос, чтобы проверить подключение
    result = db.execute(text("SELECT 1"))
    return {"db": "connected", "test": result.scalar()}