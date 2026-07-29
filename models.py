from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__="Products"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    price=Column(Integer)
    owner_id = Column(Integer, ForeignKey("Users.id"))
    owner = relationship("User", back_populates="products")

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship(
        "Item",
        back_populates="owner",
        cascade="all, delete"
    )