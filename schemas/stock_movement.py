from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from enums.stock_movement_type import StockMovementType


class StockMovementCreate(BaseModel):
    product_id: int
    type: StockMovementType
    quantity: int
    note: str | None = None


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    type: StockMovementType
    quantity: int
    note: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True