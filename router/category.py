from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_admin
from models.category import Category
from models.user import User
from schemas.category import CategoryCreate, CategoryResponse
from core.exception import (
    NotFoundException,
    BadRequestException,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    existing_category = db.query(Category).filter(
        Category.name == category.name
    ).first()

    if existing_category:
        raise BadRequestException("Category already exists")

    new_category = Category(
        name=category.name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).all()


@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise NotFoundException("Category not found")

    if category.products:
        raise BadRequestException("Cannot delete category with products")

    db.delete(category)
    db.commit()

