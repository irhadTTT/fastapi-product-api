from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_admin
from models.category import Category
from models.user import User
from repositories import category_repository
from schemas.category import CategoryCreate, CategoryResponse
from services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return await CategoryService.create_category(category, db, current_user)


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    return await CategoryService.get_all(db)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    await CategoryService.delete_category(category_id, db, current_user)
