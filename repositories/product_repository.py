from sqlalchemy.orm import Session

from models.product import Item


def get_all(db: Session):
    return db.query(Item).all()


def get_by_id(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def get_by_owner(db: Session, owner_id: int):
    return db.query(Item).filter(Item.owner_id == owner_id).all()


def create(db: Session, item: Item):
    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def delete(db: Session, item: Item):
    db.delete(item)
    db.commit()


def save(db: Session, item: Item):
    db.commit()
    db.refresh(item)

    return item


def query_items(db: Session):
    return db.query(Item)


def save_product(db: Session, product: Item):
    db.add(product)
    return product
