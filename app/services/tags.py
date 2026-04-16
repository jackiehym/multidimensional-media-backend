from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Tag, MediaItem
from app.schemas import TagCreate, TagUpdate
from app.utils.filename_parser import get_tag_category_for_name


class TagService:
    @staticmethod
    def get_tags(db: Session, skip: int = 0, limit: int = 100):
        tags = db.query(Tag).offset(skip).limit(limit).all()
        # Convert Tag objects to dictionaries
        return [{
            "id": tag.id,
            "name": tag.name,
            "category": tag.category,
            "color": tag.color,
            "created_at": tag.created_at,
            "updated_at": tag.updated_at
        } for tag in tags]

    @staticmethod
    def get_tag(db: Session, tag_id: int):
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            return None
        # Convert Tag object to dictionary
        return {
            "id": tag.id,
            "name": tag.name,
            "category": tag.category,
            "color": tag.color,
            "created_at": tag.created_at,
            "updated_at": tag.updated_at
        }

    @staticmethod
    def get_tag_by_name(db: Session, name: str) -> Optional[Tag]:
        return db.query(Tag).filter(Tag.name == name).first()

    @staticmethod
    def create_tag(db: Session, tag: TagCreate):
        try:
            db_tag = Tag(
                name=tag.name,
                category=tag.category,
                color=tag.color
            )
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
            # Convert Tag object to dictionary
            return {
                "id": db_tag.id,
                "name": db_tag.name,
                "category": db_tag.category,
                "color": db_tag.color,
                "created_at": db_tag.created_at,
                "updated_at": db_tag.updated_at
            }
        except IntegrityError:
            db.rollback()
            return None

    @staticmethod
    def update_tag(db: Session, tag_id: int, tag_update: TagUpdate):
        db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not db_tag:
            return None
        
        update_data = tag_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tag, field, value)
        
        try:
            db.commit()
            db.refresh(db_tag)
            # Convert Tag object to dictionary
            return {
                "id": db_tag.id,
                "name": db_tag.name,
                "category": db_tag.category,
                "color": db_tag.color,
                "created_at": db_tag.created_at,
                "updated_at": db_tag.updated_at
            }
        except IntegrityError:
            db.rollback()
            return None

    @staticmethod
    def delete_tag(db: Session, tag_id: int) -> bool:
        db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not db_tag:
            return False
        
        # Remove tag from all media items
        media_items = db.query(MediaItem).all()
        for media in media_items:
            if db_tag in media.tags:
                media.tags.remove(db_tag)
        
        db.delete(db_tag)
        db.commit()
        return True

    @staticmethod
    def rename_tag(db: Session, old_name: str, new_name: str) -> bool:
        old_tag = db.query(Tag).filter(Tag.name == old_name).first()
        if not old_tag:
            return False
        
        try:
            # Update tag name
            old_tag.name = new_name
            
            # Update tag in all media items
            media_items = db.query(MediaItem).all()
            for media in media_items:
                # This is handled automatically by SQLAlchemy
                pass
            
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return False

    @staticmethod
    def merge_tags(db: Session, source_names: List[str], target_name: str) -> bool:
        # Ensure target tag exists
        target_tag = db.query(Tag).filter(Tag.name == target_name).first()
        if not target_tag:
            # Create target tag if it doesn't exist
            category, color = get_tag_category_for_name(target_name)
            target_tag = Tag(
                name=target_name,
                category=category,
                color=color
            )
            db.add(target_tag)
            db.commit()
            db.refresh(target_tag)
        
        # Process source tags
        for source_name in source_names:
            if source_name == target_name:
                continue
            
            source_tag = db.query(Tag).filter(Tag.name == source_name).first()
            if not source_tag:
                continue
            
            # Replace source tag with target tag in all media items
            media_items = db.query(MediaItem).all()
            for media in media_items:
                if source_tag in media.tags:
                    media.tags.remove(source_tag)
                    if target_tag not in media.tags:
                        media.tags.append(target_tag)
            
            # Delete source tag
            db.delete(source_tag)
        
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    @staticmethod
    def bulk_delete_tags(db: Session, tag_names: List[str]) -> int:
        deleted_count = 0
        for tag_name in tag_names:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if tag:
                # Remove tag from all media items
                media_items = db.query(MediaItem).all()
                for media in media_items:
                    if tag in media.tags:
                        media.tags.remove(tag)
                
                db.delete(tag)
                deleted_count += 1
        
        db.commit()
        return deleted_count

    @staticmethod
    def change_tag_category(db: Session, tag_name: str, new_category: str) -> bool:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            return False
        
        # Get color for new category
        from app.models import TagCategory
        cat = db.query(TagCategory).filter(TagCategory.key == new_category).first()
        color = cat.color if cat else '270 60% 55%'
        
        tag.category = new_category
        tag.color = color
        
        db.commit()
        return True