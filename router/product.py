from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models.product import Item
from models.user import User
from schemas.product import ItemCreate, ItemUpdate
from dependencies import get_current_user, get_current_admin
from typing import Optional
from enums.sort import SortField, SortOrder, UserRole
import math


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# CREATE - dodavanje novog itema
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_item = Item(
        name=item.name,
        price=item.price,
        owner_id=current_user.id
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# READ - vraćanje svih itema
@router.get("/")
def get_items(
    q: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, gt=0),
    max_price: Optional[float] = Query(None, gt=0),
    sort_by: SortField | None = None,
    order: SortOrder = SortOrder.asc,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
        "products":items,
        "page":page,
        "limit":limit,
        "total":total,
        "total_pages": total_pages
    }


@router.get("/{item_id}")
def get_item(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    item = db.query(Item).filter(Item.id ==  item_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if current_user.role != UserRole.admin and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this product"
        )

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    if current_user.role != UserRole.admin and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete this product"
        )

    db.delete(item)
    db.commit()

    return


@router.put("/{item_id}")
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    db_item = db.query(Item).filter(Item.id == item_id).first()

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    if current_user.role != UserRole.admin and db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot update this product"
        )

    db_item.name = item.name
    db_item.price = item.price

    db.commit()
    db.refresh(db_item)

    return db_item