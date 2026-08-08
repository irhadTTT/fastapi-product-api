import math
import os

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.exception import BadRequestException, ForbiddenException, NotFoundException
from core.logging import logger
from core.metrics import cache_hits, cache_misses
from enums.sort import SortField, SortOrder, UserRole
from models.product import Item
from models.user import User
from repositories import product_repository
from schemas.product import ItemCreate, ItemUpdate, ProductsResponse
from services.cache_service import delete_cache_pattern, get_cache, set_cache


class ProductService:
    @staticmethod
    async def create_item(item: ItemCreate, db: Session, current_user: User):

        new_item = Item(
            name=item.name,
            price=item.price,
            owner_id=current_user.id,
            category_id=item.category_id,
        )

        created_item = product_repository.create(db, new_item)

        logger.info(
            "Product created product_id=%s name=%s created_by=%s",
            created_item.id,
            created_item.name,
            current_user.id,
        )

        await delete_cache_pattern("products:*")

        logger.debug(
            "Products cache invalidated pattern=%s action=%s", "products:*", "create"
        )

        return created_item

    @staticmethod
    async def get_items(
        db: Session, q, min_price, max_price, sort_by, order, page, limit, current_user
    ) -> ProductsResponse:

        cache_key = (
            f"products:"
            f"user:{current_user.id}:"
            f"q:{q}:"
            f"min:{min_price}:"
            f"max:{max_price}:"
            f"sort:{sort_by}:"
            f"order:{order}:"
            f"page:{page}:"
            f"limit:{limit}"
        )

        cached = await get_cache(cache_key)

        if cached:
            cache_hits.labels(resource="products").inc()
            logger.debug("Products fetched from cache count=%s", len(cached))
            return ProductsResponse(**cached)

        cache_misses.labels(resource="products").inc()

        query = db.query(Item)

        if current_user.role != UserRole.admin:
            query = query.filter(Item.owner_id == current_user.id)

        if q:
            query = query.filter(Item.name.ilike(f"%{q}%"))

        if min_price:
            query = query.filter(Item.price >= min_price)

        if max_price:
            query = query.filter(Item.price <= max_price)

        if sort_by == SortField.price:
            if order == SortOrder.desc:
                query = query.order_by(Item.price.desc())
            else:
                query = query.order_by(Item.price.asc())
        elif sort_by == SortField.name:
            if order == SortOrder.desc:
                query = query.order_by(Item.name.desc())
            else:
                query = query.order_by(Item.name.asc())
        elif sort_by == SortField.created_at:
            if order == SortOrder.desc:
                query = query.order_by(Item.created_at.desc())
            else:
                query = query.order_by(Item.created_at.asc())

        skip = (page - 1) * limit
        total = query.count()

        items = query.offset(skip).limit(limit).all()

        total_pages = math.ceil(total / limit)

        logger.info("Products fetched from database count=%s", len(items))

        response = ProductsResponse(
            products=items, page=page, limit=limit, total=total, total_pages=total_pages
        )

        await set_cache(cache_key, response, expire=300)

        logger.debug("Products cache updated count=%s", len(response.products))

        return response

    @staticmethod
    def get_item(item_id: int, db: Session, current_user: User):

        item = product_repository.get_by_id(item_id, db)

        if item is None:
            logger.warning(
                "Product not found product_id=%s user_id=%s", item_id, current_user.id
            )
            raise NotFoundException("Product not found")

        if current_user.role != UserRole.admin and item.owner_id != current_user.id:
            logger.warning(
                "Product cannot be accessed product_id=%s user_id=%s user_role=%s",
                item_id,
                current_user.id,
                current_user.role,
            )
            raise ForbiddenException("You cannot access this product")

        logger.info(
            "Product retrieved successfully product_id=%s product_name=%s",
            item.id,
            item.name,
        )
        return item

    @staticmethod
    async def delete_item(item_id: int, db: Session, current_user: User):

        item = product_repository.get_by_id(db, item_id)

        if item is None:
            logger.warning(
                "Product not found product_id=%s user_id=%s", item_id, current_user.id
            )
            raise NotFoundException("Product not found")

        if current_user.role != UserRole.admin and item.owner_id != current_user.id:
            logger.warning(
                "Product cannot be accessed product_id=%s user_id=%s user_role=%s",
                item_id,
                current_user.id,
                current_user.role,
            )
            raise ForbiddenException("You cannot delete this product")

        if item.image_url:
            image_path = item.image_url.lstrip("/")
            if os.path.exists(image_path):
                os.remove(image_path)

        product_repository.delete(db, item)

        logger.info(
            "Product deleted product_id=%s deleted_by=%s", item.id, current_user.id
        )
        await delete_cache_pattern("products:*")

        logger.debug(
            "Products cache invalidated pattern=%s action=%s", "products:*", "delete"
        )

    @staticmethod
    async def update_item(
        item_id: int, item: ItemUpdate, db: Session, current_user: User
    ):
        db_item = product_repository.get_by_id(db, item_id)

        if db_item is None:
            logger.warning(
                "Product not found product_id=%s user_id=%s", item_id, current_user.id
            )
            raise NotFoundException("Product not found")

        if current_user.role != UserRole.admin and db_item.owner_id != current_user.id:
            logger.warning(
                "Product cannot be accessed product_id=%s user_id=%s user_role=%s",
                db_item.id,
                current_user.id,
                current_user.role,
            )
            raise ForbiddenException("You cannot update this product")

        db_item.name = item.name
        db_item.price = item.price
        db_item.category_id = item.category_id

        saved = product_repository.save(db, db_item)

        logger.info(
            "Product updated product_id=%s updated_by=%s", saved.id, current_user.id
        )

        await delete_cache_pattern("products:*")

        logger.debug(
            "Product cache invalidated pattern=%s action=%s", "products:*", "update"
        )

        return saved

    @staticmethod
    async def upload_product_image(
        product_id: int, file: UploadFile, db: Session, current_user: User
    ):
        product = product_repository.get_by_id(db, product_id)

        if not product:
            logger.warning(
                "Product not found product_id=%s user_id=%s",
                product_id,
                current_user.id,
            )
            raise NotFoundException("Product not found")

        if product.owner_id != current_user.id and current_user.role != UserRole.admin:
            logger.warning(
                "Product cannot be accessed product_id=%s user_id=%s user_role=%s",
                product_id,
                current_user.id,
                current_user.role,
            )
            raise ForbiddenException("Not enough permissions")

        allowed_types = ["image/jpeg", "image/png"]

        if file.content_type not in allowed_types:
            logger.warning(
                "Only jpg and png images are allowed product_id=%s product_name=%s user_id=%s",
                product_id,
                product.name,
                current_user.id,
            )
            raise BadRequestException("Only jpg and png images are allowed")

        MAX_FILE_SIZE = 5 * 1024 * 1024

        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            logger.warning(
                "Image size must not exceed 5 MB product_id=%s product_name=%s user_id=%s",
                product_id,
                product.name,
                current_user.id,
            )
            raise BadRequestException("Image size must not exceed 5 MB.")

        file_location = f"uploads/products/{file.filename}"

        async with aiofiles.open(file_location, "wb") as buffer:
            await buffer.write(content)

        product.image_url = file_location

        db.commit()
        db.refresh(product)

        logger.info(
            "Product image uploaded product_id=%s uploaded_by=%s",
            product.id,
            current_user.id,
        )

        return {
            "message": "Image uploaded successfully",
            "image_url": product.image_url,
        }
