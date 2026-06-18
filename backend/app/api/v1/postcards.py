from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_user
from app.models import Postcard, User
from app.schemas.postcard import PostcardTemplate, PostcardCreate, PostcardOut

router = APIRouter(prefix="/postcards", tags=["postcards"])

TEMPLATES = [
    PostcardTemplate(id=1, name="Флаг России", image_url="/static/postcards/flag.png"),
    PostcardTemplate(id=2, name="Кремль", image_url="/static/postcards/kremlin.png"),
    PostcardTemplate(id=3, name="Берёзовая роща", image_url="/static/postcards/birch.png"),
]


@router.get("/templates", response_model=list[PostcardTemplate])
def templates():
    return TEMPLATES


@router.post("/", response_model=PostcardOut, status_code=201)
def create_postcard(payload: PostcardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    image_url = f"/static/postcards/generated/{payload.template_id}_{current_user.id}.png"
    postcard = Postcard(
        user_id=current_user.id,
        template_id=payload.template_id,
        sender_name=payload.sender_name,
        text=payload.text,
        image_url=image_url,
    )
    db.add(postcard)
    db.commit()
    db.refresh(postcard)
    return postcard
