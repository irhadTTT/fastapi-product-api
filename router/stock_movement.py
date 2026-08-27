from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.stock_movement import StockMovement
from models.user import User
from repositories import stock_movement_repository
from schemas.stock_movement import (
    StockMovementCreate,
    StockMovementResponse,
    StockMovementsResponse,
)
from services.stock_movement import StockMovementService

router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


@router.get("/", response_model=StockMovementsResponse)
async def get_stock_movements(
    page: int = 1, limit: int = 10, db: Session = Depends(get_db)
):
    return await StockMovementService.get_all_stock_movements(db, page, limit)


@router.post(
    "/",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_stock_movement(
    data: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    return await StockMovementService.create(db, data, current_user, idempotency_key)


@router.get("/product/{product_id}", response_model=list[StockMovementResponse])
async def get_by_product_id(product_id: int, db: Session = Depends(get_db)):
    return await StockMovementService.get_stock_history_product(product_id, db)


@router.get("/user/{user_id}", response_model=list[StockMovementResponse])
async def get_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return await StockMovementService.get_stock_history_user(user_id, db)
