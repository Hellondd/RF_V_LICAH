from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostcardTemplate(BaseModel):
    id: int
    name: str
    image_url: str


class PostcardCreate(BaseModel):
    template_id: int
    sender_name: str
    text: str


class PostcardOut(BaseModel):
    id: int
    template_id: int
    sender_name: str | None = None
    text: str | None = None
    image_url: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
