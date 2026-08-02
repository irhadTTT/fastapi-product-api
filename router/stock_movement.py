from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.stock_movement import StockMovement
from models.user import User
from repositories import stock_movement_repository
from schemas.stock_movement import StockMovementCreate, StockMovementResponse
from services.stock_movement import StockMovementService

router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"]
)

@router.get("/", response_model=list[StockMovementResponse])
def get_stock_movements(
    db: Session = Depends(get_db)
):
    return stock_movement_repository.get_all(db)

@router.post(
    "/",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED
)
def create_stock_movement(
    data: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StockMovementService.create(db, data, current_user)


@router.get(
    "/product/{product_id}",
    response_model=list[StockMovementResponse]
)
def get_product_stock_history(
    product_id: int,
    db: Session = Depends(get_db)
):

    return stock_movement_repository.get_by_product_id(db, product_id)


@router.get(
    "/user/{user_id}",
    response_model=list[StockMovementResponse]
)
def get_user_stock_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    return stock_movement_repository.get_by_user_id(db, user_id)
