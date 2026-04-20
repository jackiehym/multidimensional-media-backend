from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class MediaBase(BaseModel):
    filename: str  # 存储文件名（UUID）
    display_name: Optional[str] = None  # 显示文件名（原始文件名）
    path: str
    tags: List[str] = []
    year: Optional[int] = None
    resolution: Optional[str] = None
    rating: Optional[int] = None


class MediaCreate(MediaBase):
    pass


class MediaUpdate(BaseModel):
    filename: Optional[str] = None
    display_name: Optional[str] = None
    tags: Optional[List[str]] = None
    year: Optional[int] = None
    resolution: Optional[str] = None
    rating: Optional[int] = None


class MediaInDB(MediaBase):
    id: int
    added_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MediaResponse(MediaInDB):
    pass


class BulkMediaCreate(BaseModel):
    items: List[MediaCreate]


class BulkMediaDelete(BaseModel):
    ids: List[int]


class BulkOperationResponse(BaseModel):
    success: bool
    count: int