from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    products = relationship("Item", back_populates="owner", cascade="all, delete")
    role = Column(String, default="user")
    is_verified = Column(Boolean, default=False)
    stock_movements = relationship("StockMovement", back_populates="user")

    password_reset_tokens = relationship(
        "PasswordResetToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )
