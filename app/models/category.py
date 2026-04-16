from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from app.db.base import Base


class TagCategory(Base):
    __tablename__ = "tag_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(50), nullable=False, unique=True)
    label = Column(String(100), nullable=False)
    emoji = Column(String(10), nullable=False)
    color = Column(String(50), nullable=False)
    built_in = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())