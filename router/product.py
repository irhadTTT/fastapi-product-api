import math
import os

import aiofiles
from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from core.exception import BadRequestException, ForbiddenException, NotFoundException
from database import get_db
from dependencies import get_current_admin, get_current_user
from enums.sort import SortField, SortOrder, UserRole
from models.product import Item
from models.user import User
from schemas.product import ItemCreate, ItemUpdate, ProductsResponse
from services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProductService.create_item(item, db, current_user)


@router.get("/", response_model=ProductsResponse)
async def get_items(
    q: str | None = Query(None),
    min_price: float | None = Query(None, gt=0),
    max_price: float | None = Query(None, gt=0),
    sort_by: SortField | None = None,
    order: SortOrder = SortOrder.asc,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProductService.get_items(
        db, q, min_price, max_price, sort_by, order, page, limit, current_user
    )


@router.get("/{item_id}")
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ProductService.get_item(item_id, db, current_user)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await ProductService.delete_item(item_id, db, current_user)


@router.put("/{item_id}")
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProductService.update_item(item_id, item, db, current_user)


# upload image
@router.post("/{product_id}/image")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProductService.upload_product_image(product_id, file, db, current_user)
