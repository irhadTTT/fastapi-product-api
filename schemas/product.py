from pydantic import BaseModel, Field
from datetime import datetime
from schemas.category import CategoryResponse


class ItemCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50
    )
    price: float= Field(
        gt=0
    )
    category_id: int | None = None

class ItemUpdate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50
    )
    price: float= Field(
        gt=0
    )
    category_id: int | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: int
    image_url: str | None = None
    category: CategoryResponse | None = None
    created_at: datetime | None = None
    #AutoMapper entity-DTO kao i kod .net
    class Config:
        from_attributes = True
        #dozvoli mapiranje Entity-DTO


class ProductsResponse(BaseModel):
    products: list[ItemResponse]
    page: int
    limit: int
    total: int
    total_pages: int
    
    class Config:
        from_attributes = True