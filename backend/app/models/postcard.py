from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class PostcardTemplate(Base):
    __tablename__ = "postcard_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    postcards = relationship("Postcard", back_populates="template", cascade="all, delete-orphan")


class Postcard(Base):
    __tablename__ = "postcards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    template_id = Column(Integer, ForeignKey("postcard_templates.id", ondelete="CASCADE"), nullable=False)  # ИЗМЕНЕНО
    sender_name = Column(String(120))
    text = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="postcards")
    template = relationship("PostcardTemplate", back_populates="postcards")  # ДОБАВЛЕНО