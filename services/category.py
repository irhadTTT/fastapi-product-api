from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    NotFoundException,
)
from core.logging import logger
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
            logger.debug("Categories fetched from cache count=%s", len(cached))

            return [CategoryResponse.model_validate(category) for category in cached]

        categories = category_repository.get_all(db)

        logger.info("Categories fetched from database count=%s", len(categories))

        response = [
            CategoryResponse.model_validate(category) for category in categories
        ]

        await set_cache(
            cache_key,
            [category.model_dump(mode="json") for category in response],
            expire=300,
        )

        logger.debug("Categories cache updated count=%s", len(response))

        return response

    @staticmethod
    async def create_category(
        category: CategoryCreate, db: Session, current_user: User
    ):
        existing_category = category_repository.get_by_name(db, category.name)

        if existing_category:
            logger.warning(
                "Category creation failed, already exists name=%s user_id=%s",
                category.name,
                current_user.id,
            )
            raise BadRequestException("Category already exists")

        new_category = Category(name=category.name)
        created = category_repository.create(db, new_category)

        logger.info(
            "Category created category_id=%s name=%s created_by=%s",
            created.id,
            created.name,
            current_user.id,
        )

        await delete_cache_pattern("categories:*")

        logger.debug(
            "Category cache invalidated after creation pattern=%s action=%s",
            "categories:*",
            "create",
        )
        return created

    @staticmethod
    async def delete_category(category_id: int, db: Session, current_user: User):
        category = category_repository.get_by_id(db, category_id)

        if not category:
            logger.warning(
                "Category not found category_id=%s user_id=%s",
                category_id,
                current_user.id,
            )
            raise NotFoundException("Category not found")

        if category.products:
            logger.warning(
                "Category deletion blocked because products exist category_id=%s user_id=%s",
                category.name,
                current_user.id,
            )
            raise BadRequestException("Cannot delete category with products")

        category_repository.delete(db, category)

        await delete_cache_pattern("categories:*")

        logger.debug(
            "Category cache invalidated after deletion pattern=%s action=%s",
            "categories:*",
            "delete",
        )
