from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50
    )
    price: float= Field(
        gt=0
    )

class ItemUpdate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50
    )
    price: float= Field(
        gt=0
    )

class ItemResponse(BaseModel):
    id: int
    name: str
    price: int
#AutoMapper entity-DTO kao i kod .net
    class Config:
        from_attributes = True
        #dozvoli mapiranje Entity-DTO

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class PasswordReset(BaseModel):
    new_password: str