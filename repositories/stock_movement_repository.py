from sqlalchemy.orm import Session, joinedload

from models.stock_movement import StockMovement


def get_all(db: Session, page: int = 1, limit: int = 10):

    query = db.query(StockMovement).options(joinedload(StockMovement.product))

    total = query.count()
    offset = (page - 1) * limit

    movements = query.offset(offset).limit(limit).all()

    return movements, total


def get_by_product_id(db: Session, product_id: int):
    return (
        db.query(StockMovement)
        .filter(StockMovement.product_id == product_id)
        .order_by(StockMovement.created_at.desc())
        .all()
    )


def get_by_user_id(db: Session, user_id: int):
    return (
        db.query(StockMovement)
        .filter(StockMovement.user_id == user_id)
        .order_by(StockMovement.created_at.desc())
        .all()
    )


def get_by_id(db: Session, stock_movement_id: int):
    return (
        db.query(StockMovement)
        .filter(StockMovement.id == stock_movement_id)
        .order_by(StockMovement.created_at.desc())
        .first()
    )


def create(db: Session, movement: StockMovement):
    db.add(movement)
    return movement
