from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

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