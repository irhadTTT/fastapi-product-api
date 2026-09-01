import pandas as pd


def calculate_safety_stock(
    demand: pd.Series,
    lead_time_days: int = 7,
) -> float:
    return float(demand.std() * (lead_time_days**0.5))


def calculate_reorder_quantity(
    current_stock: int,
    forecasted_demand: float,
    safety_stock: float,
) -> int:
    required_stock = forecasted_demand + safety_stock

    reorder_quantity = required_stock - current_stock

    return max(0, round(reorder_quantity))


def get_reorder_recommendation(
    predictions_df: pd.DataFrame,
    demand: pd.Series,
    current_stock: int,
    lead_time_days: int = 7,
) -> int:
    forecasted_demand = predictions_df["predicted_demand"].sum()

    safety_stock = calculate_safety_stock(
        demand,
        lead_time_days,
    )

    return calculate_reorder_quantity(
        current_stock,
        forecasted_demand,
        safety_stock,
    )
