from sqlalchemy.orm import Session

from models.idempotency_key import IdempotencyKey


def get_by_key(db: Session, idempotency_key: int):
    return (
        db.query(IdempotencyKey)
        .filter(IdempotencyKey.key == idempotency_key)
        .order_by(IdempotencyKey.created_at.desc())
        .first()
    )
