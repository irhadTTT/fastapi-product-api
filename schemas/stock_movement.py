from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from enums.stock_movement_type import StockMovementType

from .product import ProductBasicResponse


class StockMovementCreate(BaseModel):
    product_id: int
    type: StockMovementType
    quantity: int
    note: str | None = None


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    product: ProductBasicResponse
    user_id: int
    type: StockMovementType
    quantity: int
    note: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class StockMovementsResponse(BaseModel):
    movements: list[StockMovementResponse]
    page: int
    limit: int
    total: int
    total_pages: int
