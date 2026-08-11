from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_movement_id = Column(
        Integer,
        ForeignKey("stock_movements.id"),
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
