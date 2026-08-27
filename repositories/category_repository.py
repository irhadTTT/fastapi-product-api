from sqlalchemy.orm import Session

from models.category import Category


def get_all(db: Session, page, limit):
    query = db.query(Category)

    total = query.count()
    offset = (page - 1) * limit

    categories = query.offset(offset).limit(limit).all()

    return categories, total


def get_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def create(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def delete(db: Session, category: Category):
    db.delete(category)
    db.commit()
