from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, func
from app.database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    federal_district = Column(String(120), index=True)
    capital = Column(String(120))
    short_description = Column(Text)
    full_description = Column(Text)
    facts = Column(JSON)
    culture = Column(Text)
    achievements = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
