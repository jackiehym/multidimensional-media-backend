from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import MediaItem, Tag
from app.schemas import MediaCreate, MediaUpdate


class MediaService:
    @staticmethod
    def get_media_items(db: Session, skip: int = 0, limit: int = 100):
        media_items = db.query(MediaItem).offset(skip).limit(limit).all()
        # Convert Tag objects to tag names
        result = []
        for item in media_items:
            item_dict = {
                "id": item.id,
                "filename": item.filename,
                "display_name": item.display_name,  # 显示文件名
                "path": item.path,
                "tags": [tag.name for tag in item.tags],
                "year": item.year,
                "resolution": item.resolution,
                "rating": item.rating,
                "added_at": item.added_at,
                "updated_at": item.updated_at
            }
            result.append(item_dict)
        return result

    @staticmethod
    def get_media_item(db: Session, media_id: int):
        item = db.query(MediaItem).filter(MediaItem.id == media_id).first()
        if not item:
            return None
        # Convert Tag objects to tag names
        return {
            "id": item.id,
            "filename": item.filename,
            "display_name": item.display_name,  # 显示文件名
            "path": item.path,
            "tags": [tag.name for tag in item.tags],
            "year": item.year,
            "resolution": item.resolution,
            "rating": item.rating,
            "added_at": item.added_at,
            "updated_at": item.updated_at
        }

    @staticmethod
    def create_media_item(db: Session, media: MediaCreate):
        # Handle duplicate display_name
        display_name = media.display_name
        if display_name:
            # Check if display_name already exists
            existing = db.query(MediaItem).filter(MediaItem.display_name == display_name).first()
            if existing:
                # Generate new display_name with timestamp (including milliseconds)
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')[:14]  # 精确到秒
                name_parts = display_name.rsplit('.', 1)
                if len(name_parts) > 1:
                    display_name = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
                else:
                    display_name = f"{display_name}_{timestamp}"
        
        # Ensure tags exist
        tag_objects = []
        for tag_name in set(media.tags):
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                # Create new tag
                from app.models import TagCategory
                cat = db.query(TagCategory).filter(TagCategory.key == 'custom').first()
                category = 'custom'
                color = cat.color if cat else '270 60% 55%'
                tag = Tag(
                    name=tag_name,
                    category=category,
                    color=color
                )
                db.add(tag)
                db.commit()
                db.refresh(tag)
            tag_objects.append(tag)
        
        # Create media item
        db_media = MediaItem(
            filename=media.filename,
            display_name=display_name,  # 显示文件名（可能已添加时间戳）
            path=media.path,
            tags=tag_objects,
            year=media.year,
            resolution=media.resolution,
            rating=media.rating
        )
        
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
        
        # Convert to dictionary with tag names
        return {
            "id": db_media.id,
            "filename": db_media.filename,
            "display_name": db_media.display_name,  # 显示文件名
            "path": db_media.path,
            "tags": [tag.name for tag in db_media.tags],
            "year": db_media.year,
            "resolution": db_media.resolution,
            "rating": db_media.rating,
            "added_at": db_media.added_at,
            "updated_at": db_media.updated_at
        }

    @staticmethod
    def bulk_create_media_items(db: Session, media_items: List[MediaCreate]) -> int:
        created_count = 0
        for media in media_items:
            try:
                MediaService.create_media_item(db, media)
                created_count += 1
            except IntegrityError:
                db.rollback()
                continue
        return created_count

    @staticmethod
    def update_media_item(db: Session, media_id: int, media_update: MediaUpdate):
        db_media = db.query(MediaItem).filter(MediaItem.id == media_id).first()
        if not db_media:
            return None
        
        update_data = media_update.model_dump(exclude_unset=True)
        
        if 'display_name' in update_data:
            new_display_name = update_data['display_name']
            if new_display_name is not None:
                existing = db.query(MediaItem).filter(
                    MediaItem.display_name == new_display_name,
                    MediaItem.id != media_id
                ).first()
                if existing:
                    raise ValueError(f"Display name '{new_display_name}' already exists")
        
        if 'tags' in update_data:
            tag_objects = []
            for tag_name in update_data.pop('tags'):
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    from app.models import TagCategory
                    cat = db.query(TagCategory).filter(TagCategory.key == 'custom').first()
                    category = 'custom'
                    color = cat.color if cat else '270 60% 55%'
                    tag = Tag(
                        name=tag_name,
                        category=category,
                        color=color
                    )
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                tag_objects.append(tag)
            db_media.tags = tag_objects
        
        for field, value in update_data.items():
            setattr(db_media, field, value)
        
        db.commit()
        db.refresh(db_media)
        
        return {
            "id": db_media.id,
            "filename": db_media.filename,
            "display_name": db_media.display_name,
            "path": db_media.path,
            "tags": [tag.name for tag in db_media.tags],
            "year": db_media.year,
            "resolution": db_media.resolution,
            "rating": db_media.rating,
            "added_at": db_media.added_at,
            "updated_at": db_media.updated_at
        }

    @staticmethod
    def delete_media_item(db: Session, media_id: int) -> bool:
        db_media = db.query(MediaItem).filter(MediaItem.id == media_id).first()
        if not db_media:
            return False
        
        # 提取文件名并删除物理文件
        try:
            from app.services.storage import StorageService
            # 从 path 中提取文件名（如 "/media/123.mp4" -> "123.mp4"）
            filename = db_media.path.split('/')[-1]
            StorageService.delete_file(filename)
        except Exception:
            # 文件删除失败不影响数据库删除
            pass
        
        db.delete(db_media)
        db.commit()
        return True

    @staticmethod
    def bulk_delete_media_items(db: Session, media_ids: List[int]) -> int:
        # 先获取所有要删除的媒体项
        media_items = db.query(MediaItem).filter(MediaItem.id.in_(media_ids)).all()
        
        # 遍历删除物理文件
        try:
            from app.services.storage import StorageService
            for media in media_items:
                # 从 path 中提取文件名
                filename = media.path.split('/')[-1]
                StorageService.delete_file(filename)
        except Exception:
            # 文件删除失败不影响数据库删除
            pass
        
        # 删除数据库记录
        deleted_count = db.query(MediaItem).filter(MediaItem.id.in_(media_ids)).delete(synchronize_session=False)
        db.commit()
        return deleted_count

    @staticmethod
    def add_tag_to_items(db: Session, media_ids: List[int], tag_name: str, category: Optional[str] = None) -> bool:
        # Ensure tag exists
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            if not category:
                category = 'custom'
            
            from app.models import TagCategory
            cat = db.query(TagCategory).filter(TagCategory.key == category).first()
            color = cat.color if cat else '270 60% 55%'
            
            tag = Tag(
                name=tag_name,
                category=category,
                color=color
            )
            db.add(tag)
            db.flush()  # 刷新以获取 ID，但不提交事务
        
        # Add tag to media items
        media_items = db.query(MediaItem).filter(MediaItem.id.in_(media_ids)).all()
        for media in media_items:
            # 检查标签是否已存在（使用标签名称进行比较）
            tag_exists = any(t.name == tag_name for t in media.tags)
            if not tag_exists:
                media.tags.append(tag)
        
        return True

    @staticmethod
    def remove_tag_from_items(db: Session, media_ids: List[int], tag_name: str) -> bool:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            return False
        
        media_items = db.query(MediaItem).filter(MediaItem.id.in_(media_ids)).all()
        for media in media_items:
            # 使用标签名称进行比较，而不是对象引用
            tag_to_remove = next((t for t in media.tags if t.name == tag_name), None)
            if tag_to_remove:
                media.tags.remove(tag_to_remove)
        
        return True