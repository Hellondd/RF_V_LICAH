from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(120), index=True)
    description = Column(Text)
    year_or_period = Column(String(120))
    image_url = Column(String(500))
    source = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
