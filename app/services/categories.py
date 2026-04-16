from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import TagCategory, Tag
from app.schemas import CategoryCreate, CategoryUpdate


class CategoryService:
    @staticmethod
    def get_categories(db: Session):
        categories = db.query(TagCategory).all()
        # Convert TagCategory objects to dictionaries
        return [{
            "id": cat.id,
            "key": cat.key,
            "label": cat.label,
            "emoji": cat.emoji,
            "color": cat.color,
            "built_in": cat.built_in,
            "created_at": cat.created_at,
            "updated_at": cat.updated_at
        } for cat in categories]

    @staticmethod
    def get_category(db: Session, category_id: int):
        cat = db.query(TagCategory).filter(TagCategory.id == category_id).first()
        if not cat:
            return None
        # Convert TagCategory object to dictionary
        return {
            "id": cat.id,
            "key": cat.key,
            "label": cat.label,
            "emoji": cat.emoji,
            "color": cat.color,
            "built_in": cat.built_in,
            "created_at": cat.created_at,
            "updated_at": cat.updated_at
        }

    @staticmethod
    def get_category_by_key(db: Session, key: str) -> Optional[TagCategory]:
        return db.query(TagCategory).filter(TagCategory.key == key).first()

    @staticmethod
    def create_category(db: Session, category: CategoryCreate):
        try:
            db_category = TagCategory(
                key=category.key,
                label=category.label,
                emoji=category.emoji,
                color=category.color,
                built_in=False
            )
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            # Convert TagCategory object to dictionary
            return {
                "id": db_category.id,
                "key": db_category.key,
                "label": db_category.label,
                "emoji": db_category.emoji,
                "color": db_category.color,
                "built_in": db_category.built_in,
                "created_at": db_category.created_at,
                "updated_at": db_category.updated_at
            }
        except IntegrityError:
            db.rollback()
            return None

    @staticmethod
    def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
        db_category = db.query(TagCategory).filter(TagCategory.id == category_id).first()
        if not db_category:
            return None
        
        update_data = category_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        
        db.commit()
        db.refresh(db_category)
        # Convert TagCategory object to dictionary
        return {
            "id": db_category.id,
            "key": db_category.key,
            "label": db_category.label,
            "emoji": db_category.emoji,
            "color": db_category.color,
            "built_in": db_category.built_in,
            "created_at": db_category.created_at,
            "updated_at": db_category.updated_at
        }

    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        db_category = db.query(TagCategory).filter(TagCategory.id == category_id).first()
        if not db_category:
            return False
        
        # Check if it's a built-in category
        if db_category.built_in:
            return False
        
        # Move all tags in this category to 'custom'
        tags = db.query(Tag).filter(Tag.category == db_category.key).all()
        for tag in tags:
            tag.category = 'custom'
            # Update color to custom category color
            custom_cat = db.query(TagCategory).filter(TagCategory.key == 'custom').first()
            if custom_cat:
                tag.color = custom_cat.color
        
        db.delete(db_category)
        db.commit()
        return True

    @staticmethod
    def seed_default_categories(db: Session) -> None:
        default_categories = [
            {"key": "genre", "label": "类型", "emoji": "🎬", "color": "210 70% 50%", "built_in": True},
            {"key": "quality", "label": "画质", "emoji": "📺", "color": "150 60% 40%", "built_in": True},
            {"key": "year", "label": "年份", "emoji": "📅", "color": "220 10% 50%", "built_in": True},
            {"key": "custom", "label": "自定义", "emoji": "🏷️", "color": "270 60% 55%", "built_in": True},
        ]
        
        for cat_data in default_categories:
            existing = db.query(TagCategory).filter(TagCategory.key == cat_data["key"]).first()
            if not existing:
                category = TagCategory(**cat_data)
                db.add(category)
        
        db.commit()

    @staticmethod
    def seed_default_tags(db: Session) -> None:
        # First seed default categories
        CategoryService.seed_default_categories(db)
        
        default_tags = [
            {"name": "4K", "category": "quality", "color": "150 60% 40%"},
            {"name": "1080p", "category": "quality", "color": "150 60% 40%"},
            {"name": "720p", "category": "quality", "color": "150 60% 40%"},
            {"name": "Action", "category": "genre", "color": "210 70% 50%"},
            {"name": "Sci-Fi", "category": "genre", "color": "210 70% 50%"},
            {"name": "Drama", "category": "genre", "color": "210 70% 50%"},
            {"name": "Comedy", "category": "genre", "color": "210 70% 50%"},
            {"name": "Horror", "category": "genre", "color": "210 70% 50%"},
            {"name": "Thriller", "category": "genre", "color": "210 70% 50%"},
            {"name": "待看", "category": "custom", "color": "270 60% 55%"},
            {"name": "已看", "category": "custom", "color": "270 60% 55%"},
            {"name": "收藏", "category": "custom", "color": "270 60% 55%"},
        ]
        
        from app.schemas import TagCreate
        for tag_data in default_tags:
            existing = db.query(Tag).filter(Tag.name == tag_data["name"]).first()
            if not existing:
                from app.services.tags import TagService
                TagService.create_tag(db, TagCreate(**tag_data))