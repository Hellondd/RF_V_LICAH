from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    category = Column(String(120), index=True)
    region = Column(String(120))
    short_bio = Column(Text)
    contribution = Column(Text)
    importance = Column(Text)
    image_url = Column(String(500))
    source = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
