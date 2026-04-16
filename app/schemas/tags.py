from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class TagBase(BaseModel):
    name: str
    category: str
    color: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    color: Optional[str] = None


class TagInDB(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TagResponse(TagInDB):
    pass


class TagRename(BaseModel):
    old_name: str
    new_name: str


class TagMerge(BaseModel):
    source_names: List[str]
    target_name: str


class TagsBulkDelete(BaseModel):
    names: List[str]


class TagOperationResponse(BaseModel):
    success: bool