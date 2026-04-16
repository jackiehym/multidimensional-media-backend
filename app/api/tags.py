from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas import (
    TagResponse, TagCreate, TagUpdate, 
    TagRename, TagMerge, TagsBulkDelete, TagOperationResponse
)
from app.services.tags import TagService

router = APIRouter()


@router.get("", response_model=List[TagResponse])
def get_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    tags = TagService.get_tags(db, skip=skip, limit=limit)
    return tags


@router.post("", response_model=TagResponse)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    db_tag = TagService.create_tag(db=db, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    return db_tag


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: Session = Depends(get_db)
):
    db_tag = TagService.update_tag(db=db, tag_id=tag_id, tag_update=tag_update)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    success = TagService.delete_tag(db=db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"success": True}


@router.post("/rename")
def rename_tag(
    rename_data: TagRename,
    db: Session = Depends(get_db)
):
    success = TagService.rename_tag(db=db, old_name=rename_data.old_name, new_name=rename_data.new_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to rename tag")
    return {"success": success}


@router.post("/merge")
def merge_tags(
    merge_data: TagMerge,
    db: Session = Depends(get_db)
):
    success = TagService.merge_tags(db=db, source_names=merge_data.source_names, target_name=merge_data.target_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to merge tags")
    return {"success": success}


@router.post("/bulk-delete")
def bulk_delete_tags(
    delete_data: TagsBulkDelete,
    db: Session = Depends(get_db)
):
    count = TagService.bulk_delete_tags(db=db, tag_names=delete_data.names)
    return {"success": True, "count": count}


@router.post("/change-category")
def change_tag_category(
    tag_name: str = Body(..., embed=True),
    new_category: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    success = TagService.change_tag_category(db=db, tag_name=tag_name, new_category=new_category)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"success": success}