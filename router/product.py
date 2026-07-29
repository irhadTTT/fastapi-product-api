from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models import Item, User
from schema import ItemCreate, ItemUpdate
from dependencies import get_current_user, get_current_admin

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# CREATE - dodavanje novog itema
@router.post("/")
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(Item).all()

    return db.query(Item).filter(
        Item.owner_id == current_user.id
    ).all()


@router.get("/{item_id}")
def get_item(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    item = db.query(Item).filter(Item.id ==  item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if current_user.role != "admin" and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this product"
        )

    return item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
        
    if current_user.role != "admin" and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this product"
        )

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}


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
            status_code=404,
            detail="Product not found"
        )
        
    if current_user.role != "admin" and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this product"
        )

    db_item.name = item.name
    db_item.price = item.price

    db.commit()
    db.refresh(db_item)

    return db_item