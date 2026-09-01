from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.forecast import DemandForecastResponse, ReorderRecommendationResponse
from services.forecast_service import ForecastService

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
)


@router.get(
    "/products/{product_id}",
    response_model=DemandForecastResponse,
)
def forecast_product_demand(product_id: int, db: Session = Depends(get_db)):
    return ForecastService.forecast_product_demand(db, product_id)


@router.get(
    "/products/{product_id}/reorder",
    response_model=ReorderRecommendationResponse,
)
def get_reorder_recommendation(product_id: int, db: Session = Depends(get_db)):
    return ForecastService.get_reorder_recommendation(db, product_id)
