from sqlalchemy.orm import Session

from models.stock_movement import StockMovement


def get_all(db: Session):
    return db.query(StockMovement).all()


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
