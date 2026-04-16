from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas import (
    CategoryResponse, CategoryCreate, CategoryUpdate, CategoryOperationResponse
)
from app.services.categories import CategoryService

router = APIRouter()


@router.get("", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    # Seed default categories if they don't exist
    CategoryService.seed_default_categories(db)
    categories = CategoryService.get_categories(db)
    return categories


@router.post("", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    db_category = CategoryService.create_category(db=db, category=category)
    if db_category is None:
        raise HTTPException(status_code=400, detail="Category with this key already exists")
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = CategoryService.update_category(db=db, category_id=category_id, category_update=category_update)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    success = CategoryService.delete_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found or cannot be deleted")
    return {"success": True}


@router.post("/seed")
def seed_default_data(
    db: Session = Depends(get_db)
):
    CategoryService.seed_default_categories(db)
    CategoryService.seed_default_tags(db)
    return {"success": True, "message": "Default data seeded successfully"}