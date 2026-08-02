from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    NotFoundException,
)
from models.category import Category
from models.user import User
from repositories import category_repository
from schemas.category import CategoryCreate


class CategoryService:

    @staticmethod
    def create_category(
        category: CategoryCreate,
        db: Session,
        current_user: User
    ):
        existing_category = category_repository.get_by_name(db, category.name)

        if existing_category:
            raise BadRequestException("Category already exists")

        new_category = Category(
            name=category.name
        )
        return category_repository.create(db, new_category)

    @staticmethod
    def delete_category(
        category_id: int,
        db: Session,
        current_user: User
    ):
        category = category_repository.get_by_id(db, category_id)

        if not category:
            raise NotFoundException("Category not found")

        if category.products:
            raise BadRequestException("Cannot delete category with products")

        category_repository.delete(db, category)