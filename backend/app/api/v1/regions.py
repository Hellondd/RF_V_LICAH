from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_admin
from app.models import Region
from app.schemas.region import RegionCreate, RegionUpdate, RegionOut

router = APIRouter(prefix="/regions", tags=["regions"])


@router.get("/", response_model=list[RegionOut])
def list_regions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(Region).offset(skip).limit(limit).all()


@router.get("/{region_id}", response_model=RegionOut)
def get_region(region_id: int, db: Session = Depends(get_db)):
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    return region


@router.post("/", response_model=RegionOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_region(payload: RegionCreate, db: Session = Depends(get_db)):
    region = Region(**payload.model_dump())
    db.add(region)
    db.commit()
    db.refresh(region)
    return region


@router.put("/{region_id}", response_model=RegionOut, dependencies=[Depends(get_current_admin)])
def update_region(region_id: int, payload: RegionUpdate, db: Session = Depends(get_db)):
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(region, field, value)
    db.commit()
    db.refresh(region)
    return region


@router.delete("/{region_id}", status_code=204, dependencies=[Depends(get_current_admin)])
def delete_region(region_id: int, db: Session = Depends(get_db)):
    region = db.query(Region).get(region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    db.delete(region)
    db.commit()
