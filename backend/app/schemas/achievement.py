from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AchievementBase(BaseModel):
    title: str
    category: str | None = None
    description: str | None = None
    year_or_period: str | None = None
    image_url: str | None = None
    source: str | None = None


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(AchievementBase):
    title: str | None = None


class AchievementOut(AchievementBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
