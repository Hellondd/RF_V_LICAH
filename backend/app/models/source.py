from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(500))
    description = Column(Text)
    content_type = Column(String(80))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
