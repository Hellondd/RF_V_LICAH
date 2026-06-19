from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_admin
from app.models import Achievement
from app.schemas.achievement import AchievementCreate, AchievementUpdate, AchievementOut

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/", response_model=list[AchievementOut])
def list_achievements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Achievement)
    if category:
        query = query.filter(Achievement.category == category)
    return query.offset(skip).limit(limit).all()


@router.get("/{achievement_id}", response_model=AchievementOut)
def get_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement = db.query(Achievement).get(achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено")
    return achievement


@router.post("/", response_model=AchievementOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_achievement(payload: AchievementCreate, db: Session = Depends(get_db)):
    achievement = Achievement(**payload.model_dump())
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    return achievement


@router.put("/{achievement_id}", response_model=AchievementOut, dependencies=[Depends(get_current_admin)])
def update_achievement(achievement_id: int, payload: AchievementUpdate, db: Session = Depends(get_db)):
    achievement = db.query(Achievement).get(achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(achievement, field, value)
    db.commit()
    db.refresh(achievement)
    return achievement


@router.delete("/{achievement_id}", status_code=204, dependencies=[Depends(get_current_admin)])
def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement = db.query(Achievement).get(achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено")
    db.delete(achievement)
    db.commit()
