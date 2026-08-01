from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    products = relationship(
        "Item",
        back_populates="owner",
        cascade="all, delete"
    )
    role = Column(String, default="user")
    is_verified = Column(
        Boolean,
        default=False
    )