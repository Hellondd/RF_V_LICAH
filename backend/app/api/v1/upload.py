import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.config import settings
from app.core.deps import get_current_admin

router = APIRouter(prefix="/upload", tags=["upload"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@router.post("/", dependencies=[Depends(get_current_admin)])
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if file.content_type not in ALLOWED_TYPES or ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Недопустимый тип файла (только изображения)")

    contents = await file.read()
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(status_code=400, detail=f"Файл больше {settings.MAX_FILE_SIZE_MB} МБ")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(contents)

    return {"url": f"/{settings.UPLOAD_DIR}/{filename}", "filename": filename}
