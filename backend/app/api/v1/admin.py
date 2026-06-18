from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_admin
from app.models import User, Region, Person, Achievement, QuizQuestion, QuizResult, Postcard
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(get_current_admin)])


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "regions": db.query(Region).count(),
        "persons": db.query(Person).count(),
        "achievements": db.query(Achievement).count(),
        "quiz_questions": db.query(QuizQuestion).count(),
        "quiz_results": db.query(QuizResult).count(),
        "postcards": db.query(Postcard).count(),
    }


@router.get("/users", response_model=list[UserOut])
def users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(User).offset(skip).limit(limit).all()
