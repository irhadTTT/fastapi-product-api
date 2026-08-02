from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from enums.stock_movement_type import StockMovementType


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    product = relationship("Item", back_populates="stock_movements")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="stock_movements")

    type = Column(Enum(StockMovementType), nullable=False)

    quantity = Column(Integer, nullable=False)

    note = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
