from datetime import date

from pydantic import BaseModel


class DemandForecastItem(BaseModel):
    date: date
    predicted_demand: float


class DemandForecastResponse(BaseModel):
    product_id: int
    forecast_days: int
    predictions: list[DemandForecastItem]
    total_predicted_demand: float


class ReorderRecommendationResponse(BaseModel):
    product_id: int
    current_stock: int
    forecasted_demand: float
    safety_stock: float
    recommended_reorder: int
