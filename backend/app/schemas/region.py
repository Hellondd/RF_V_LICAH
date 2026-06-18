from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class RegionBase(BaseModel):
    title: str
    federal_district: str | None = None
    capital: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    facts: Any | None = None
    culture: str | None = None
    achievements: str | None = None
    image_url: str | None = None


class RegionCreate(RegionBase):
    pass


class RegionUpdate(RegionBase):
    title: str | None = None


class RegionOut(RegionBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
