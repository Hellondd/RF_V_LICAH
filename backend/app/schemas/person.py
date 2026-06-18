from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PersonBase(BaseModel):
    full_name: str
    category: str | None = None
    region: str | None = None
    short_bio: str | None = None
    contribution: str | None = None
    importance: str | None = None
    image_url: str | None = None
    source: str | None = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    full_name: str | None = None


class PersonOut(PersonBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
