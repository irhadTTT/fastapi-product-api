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
    image_url: str | None = None
    
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