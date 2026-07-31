from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Item(Base):
    __tablename__="products"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    price=Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship(
        "User", 
        back_populates="products"
        )
    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )
    created_at = Column(
        DateTime,
        default = datetime.utcnow
    )
    image_url = Column(String, nullable=True)