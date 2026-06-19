from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_admin
from app.models import Person
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("/", response_model=list[PersonOut])
def list_persons(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Person)
    if category:
        query = query.filter(Person.category == category)
    return query.offset(skip).limit(limit).all()


@router.get("/{person_id}", response_model=PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).get(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Персона не найдена")
    return person


@router.post("/", response_model=PersonOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_person(payload: PersonCreate, db: Session = Depends(get_db)):
    person = Person(**payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.put("/{person_id}", response_model=PersonOut, dependencies=[Depends(get_current_admin)])
def update_person(person_id: int, payload: PersonUpdate, db: Session = Depends(get_db)):
    person = db.query(Person).get(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Персона не найдена")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(person, field, value)
    db.commit()
    db.refresh(person)
    return person


@router.delete("/{person_id}", status_code=204, dependencies=[Depends(get_current_admin)])
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).get(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Персона не найдена")
    db.delete(person)
    db.commit()
