from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import subprocess
from pydantic import BaseModel

from app.db.session import get_db
from app.schemas import (
    MediaResponse, MediaCreate, MediaUpdate, 
    BulkMediaCreate, BulkMediaDelete, BulkOperationResponse
)
from app.services.media import MediaService
from app.services.storage import StorageService

router = APIRouter()


@router.get("", response_model=List[MediaResponse])
def get_media_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    media_items = MediaService.get_media_items(db, skip=skip, limit=limit)
    return media_items


@router.get("/{media_id}", response_model=MediaResponse)
def get_media_item(
    media_id: int,
    db: Session = Depends(get_db)
):
    media_item = MediaService.get_media_item(db, media_id=media_id)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media item not found")
    return media_item


@router.post("", response_model=MediaResponse)
def create_media_item(
    media: MediaCreate,
    db: Session = Depends(get_db)
):
    return MediaService.create_media_item(db=db, media=media)


@router.post("/bulk", response_model=BulkOperationResponse)
def bulk_create_media_items(
    bulk_media: BulkMediaCreate,
    db: Session = Depends(get_db)
):
    count = MediaService.bulk_create_media_items(db=db, media_items=bulk_media.items)
    return BulkOperationResponse(success=True, count=count)


@router.put("/{media_id}", response_model=MediaResponse)
def update_media_item(
    media_id: int,
    media_update: MediaUpdate,
    db: Session = Depends(get_db)
):
    media_item = MediaService.update_media_item(db=db, media_id=media_id, media_update=media_update)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media item not found")
    return media_item


@router.delete("/{media_id}")
def delete_media_item(
    media_id: int,
    db: Session = Depends(get_db)
):
    success = MediaService.delete_media_item(db=db, media_id=media_id)
    if not success:
        raise HTTPException(status_code=404, detail="Media item not found")
    return {"success": True}


@router.post("/bulk-delete")
def bulk_delete_media_items(
    bulk_delete: BulkMediaDelete,
    db: Session = Depends(get_db)
):
    count = MediaService.bulk_delete_media_items(db=db, media_ids=bulk_delete.ids)
    return BulkOperationResponse(success=True, count=count)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    try:
        path, filename = StorageService.save_uploaded_file(file, file.filename)
        return {
            "path": path,
            "filename": filename,
            "size": file.size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-tag")
def add_tag_to_items(
    media_ids: List[int] = Body(..., embed=True),
    tag_name: str = Body(..., embed=True),
    category: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    success = MediaService.add_tag_to_items(db=db, media_ids=media_ids, tag_name=tag_name, category=category)
    db.commit()
    return {"success": success}


@router.post("/remove-tag")
def remove_tag_from_items(
    media_ids: List[int] = Body(..., embed=True),
    tag_name: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    success = MediaService.remove_tag_from_items(db=db, media_ids=media_ids, tag_name=tag_name)
    db.commit()
    return {"success": success}


class OpenFileRequest(BaseModel):
    path: str


@router.post("/open-file")
def open_file(request: OpenFileRequest):
    """打开本地文件"""
    if not os.path.exists(request.path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        if os.name == 'nt':  # Windows
            os.startfile(request.path)
        else:  # macOS/Linux
            subprocess.call(['open', request.path])
        return {"success": True, "message": "已尝试打开文件"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/open-location")
def open_location(request: OpenFileRequest):
    """打开文件所在位置"""
    if not os.path.exists(request.path):
        raise HTTPException(status_code=404, detail="文件不存在")
    print(request.path)
    try:
        if os.name == 'nt':  # Windows
            # 使用 explorer /select 打开文件夹并选中文件
            path = request.path.replace("/", "\\")
            subprocess.Popen(f'explorer /select,"{path}"')
        elif os.name == 'posix':  # macOS
            subprocess.call(['open', '-R', request.path])
        else:  # Linux
            # 打开文件所在目录
            parent_dir = os.path.dirname(request.path)
            subprocess.call(['xdg-open', parent_dir])
        return {"success": True, "message": "已打开文件位置"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))