from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    NotFoundException,
)
from models.category import Category
from models.user import User
from repositories import category_repository
from schemas.category import CategoryCreate, CategoryResponse
from services.cache_service import delete_cache_pattern, get_cache, set_cache


class CategoryService:
    @staticmethod
    async def get_all(db: Session):
        cache_key = "categories:list"

        cached = await get_cache(cache_key)

        if cached:
            return [CategoryResponse.model_validate(category) for category in cached]

        categories = category_repository.get_all(db)

        response = [
            CategoryResponse.model_validate(category) for category in categories
        ]

        await set_cache(
            cache_key,
            [category.model_dump(mode="json") for category in response],
            expire=300,
        )

        return response

    @staticmethod
    async def create_category(
        category: CategoryCreate, db: Session, current_user: User
    ):
        existing_category = category_repository.get_by_name(db, category.name)

        if existing_category:
            raise BadRequestException("Category already exists")

        new_category = Category(name=category.name)
        created = category_repository.create(db, new_category)

        await delete_cache_pattern("categories:*")

        return created

    @staticmethod
    async def delete_category(category_id: int, db: Session, current_user: User):
        category = category_repository.get_by_id(db, category_id)

        if not category:
            raise NotFoundException("Category not found")

        if category.products:
            raise BadRequestException("Cannot delete category with products")

        category_repository.delete(db, category)

        await delete_cache_pattern("categories:*")
