import math
import os

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.exception import BadRequestException, ForbiddenException, NotFoundException
from enums.sort import SortField, SortOrder, UserRole
from models.product import Item
from models.user import User
from repositories import product_repository
from schemas.product import ItemCreate, ItemUpdate, ProductsResponse


class ProductService:

    @staticmethod
    def create_item(
        item: ItemCreate,
        db: Session,
        current_user: User
    ):

        new_item = Item(
            name=item.name,
            price=item.price,
            owner_id=current_user.id,
            category_id=item.category_id
        )

        return product_repository.create(db, new_item)

    @staticmethod
    def get_items(
        db: Session,
        q,
        min_price,
        max_price,
        sort_by,
        order,
        page,
        limit,
        current_user
    ) -> ProductsResponse:

        query = db.query(Item)

        if current_user.role != UserRole.admin:
            query = query.filter(
                Item.owner_id == current_user.id
            )
        
        if q:
            query = query.filter(
                Item.name.ilike(f"%{q}%")
            )

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

        skip = (page-1)*limit
        total = query.count()

        items = (query.offset(skip).limit(limit).all())

        total_pages = math.ceil(total / limit)

        return {
            "products": items,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        }

    @staticmethod
    def get_item(
        item_id: int,
        db: Session,
        current_user: User
    ):

        item = product_repository.get_by_id(item_id, db)

        if item is None:
            raise NotFoundException("Product not found")

        if current_user.role != UserRole.admin and item.owner_id != current_user.id:
            raise ForbiddenException("You cannot access this product")
    
        return item

    @staticmethod
    def delete_item(
        item_id: int,
        db: Session,
        current_user: User
    ):

        item = product_repository.get_by_id(db, item_id)

        if item is None:
            raise NotFoundException("Product not found")
            
        if current_user.role != UserRole.admin and item.owner_id != current_user.id:
            raise ForbiddenException("You cannot delete this product")

        if item.image_url:
            image_path = item.image_url.lstrip("/")
            if os.path.exists(image_path):
                os.remove(image_path)

        product_repository.delete(db, item)

    @staticmethod
    def update_item(
        item_id: int,
        item: ItemUpdate,
        db: Session,
        current_user: User
    ):
        db_item = product_repository.get_by_id(db, item_id)

        if db_item is None:
            raise NotFoundException("Product not found")
            
        if current_user.role != UserRole.admin and db_item.owner_id != current_user.id:
            raise ForbiddenException("You cannot update this product")

        db_item.name = item.name
        db_item.price = item.price
        db_item.category_id = item.category_id
        
        return product_repository.save(db, db_item)

    @staticmethod
    async def upload_product_image(
        product_id: int,
        file: UploadFile,
        db: Session,
        current_user: User
    ):
        product = product_repository.get_by_id(db, product_id)

        if not product:
            raise NotFoundException("Product not found")

        if product.owner_id != current_user.id and current_user.role != UserRole.admin:
            raise ForbiddenException("Not enough permissions")

        allowed_types = [
            "image/jpeg",
            "image/png"
        ]

        if file.content_type not in allowed_types:
            raise BadRequestException("Only jpg and png images are allowed")

        MAX_FILE_SIZE = 5 * 1024 * 1204

        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise BadRequestException("Image size must not exceed 5 MB.")

        file_location = f"uploads/products/{file.filename}"

        async with aiofiles.open(file_location, "wb") as buffer:
            await buffer.write(content)

        product.image_url = file_location

        db.commit()
        db.refresh(product)

        return {
            "message": "Image uploaded successfully",
            "image_url": product.image_url
        }
