from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Item(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("User", back_populates="products")
    stock_quantity = Column(Integer, default=0, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    image_url = Column(String, nullable=True)

    stock_movements = relationship("StockMovement", back_populates="product")

    __table_args__ = (
        Index(
            "ix_products_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )
