from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from enums.stock_movement_type import StockMovementType
from ml.features import (
    create_features,
    create_prediction_features,
    forecast_future_demand,
    prepare_training_data,
)
from ml.forecasting import predict_demand, train_model
from models.product import Item
from models.stock_movement import StockMovement
from schemas.forecast import DemandForecastResponse
from services.forecast_service import ForecastService


@pytest.mark.asyncio
async def test_get_product_demand_history(db_session, other_user):
    product = Item(
        name="ForecastProduct",
        price=100,
        stock_quantity=100,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    base_date = datetime(2026, 8, 1, tzinfo=timezone.utc)

    movements = [
        StockMovement(
            product_id=product.id,
            user_id=other_user.id,
            type=StockMovementType.OUT,
            quantity=10,
            created_at=base_date,
        ),
        StockMovement(
            product_id=product.id,
            user_id=other_user.id,
            type=StockMovementType.OUT,
            quantity=5,
            created_at=base_date + timedelta(days=1),
        ),
        StockMovement(
            product_id=product.id,
            user_id=other_user.id,
            type=StockMovementType.OUT,
            quantity=8,
            created_at=base_date + timedelta(days=3),
        ),
    ]

    db_session.add_all(movements)
    db_session.commit()

    result = await ForecastService.get_product_demand_history(
        db_session,
        product.id,
    )

    assert len(result) == 4
    # integration location iloc daj mi ono u pandasu sto je na ovoj poziciji
    assert result.iloc[0]["demand"] == 10
    assert result.iloc[1]["demand"] == 5
    assert result.iloc[2]["demand"] == 0
    assert result.iloc[3]["demand"] == 8


def test_create_features():
    dates = pd.date_range("2026-08-01", periods=14, freq="D")

    df = pd.DataFrame(
        {
            "date": dates,
            "demand": range(1, 15),
        }
    )

    result = create_features(df)

    assert "lag_1" in result.columns
    assert "lag_7" in result.columns
    assert "rolling_mean_7" in result.columns

    assert result.iloc[1]["lag_1"] == 1
    assert result.iloc[7]["lag_7"] == 1


def test_prepare_training_data():
    dates = pd.date_range("2026-08-01", periods=14, freq="D")

    df = pd.DataFrame(
        {
            "date": dates,
            "demand": range(1, 15),
        }
    )

    result = prepare_training_data(df)

    assert len(result) == 7
    assert result.iloc[0]["demand"] == 8
    assert result.iloc[0]["lag_1"] == 7
    assert result.iloc[0]["lag_7"] == 1


def test_train_model():
    dates = pd.date_range("2026-08-01", periods=14, freq="D")

    df = pd.DataFrame(
        {
            "date": dates,
            "demand": range(1, 15),
        }
    )

    training_data = prepare_training_data(df)

    model = train_model(training_data)

    assert model is not None
    assert hasattr(model, "predict")


def test_predict_demand():
    dates = pd.date_range("2026-08-01", periods=14, freq="D")

    df = pd.DataFrame(
        {
            "date": dates,
            "demand": range(1, 15),
        }
    )

    training_data = prepare_training_data(df)

    model = train_model(training_data)
    # ovako sa dvije uglaste zagrade dobijamo Pandas DataFrame
    features = training_data.iloc[[0]]

    prediction = predict_demand(model, features)

    assert isinstance(prediction, float)
    assert prediction >= 0


def test_create_prediction_features():
    dates = pd.date_range("2026-08-01", periods=14, freq="D")

    df = pd.DataFrame(
        {
            "date": dates,
            "demand": range(1, 15),
        }
    )

    result = create_prediction_features(df)

    assert len(result) == 1
    assert result.iloc[0]["date"] == pd.Timestamp("2026-08-15")
    assert result.iloc[0]["lag_1"] == 14
    assert result.iloc[0]["lag_7"] == 8
    assert result.iloc[0]["day_of_week"] == 5


def test_forecast_product_demand(
    db_session,
    other_user,
):
    product = Item(
        name="Forecast Product",
        price=100,
        stock_quantity=50,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    today = datetime.now(timezone.utc)

    for i in range(14):
        movement = StockMovement(
            product_id=product.id,
            user_id=other_user.id,
            type=StockMovementType.OUT,
            quantity=i + 1,
            created_at=today - timedelta(days=13 - i),
        )

        db_session.add(movement)

    db_session.commit()

    result = ForecastService.forecast_product_demand(db_session, product.id)

    assert isinstance(result, DemandForecastResponse)
    assert result.product_id == product.id
    assert result.forecast_days == 30
    assert len(result.predictions) == 30
    assert result.predictions[0].predicted_demand >= 0
    assert result.total_predicted_demand >= 0


def test_forecast_future_demand():
    dates = pd.date_range(
        start="2026-08-01",
        periods=14,
        freq="D",
    )

    demand_df = pd.DataFrame(
        {
            "date": dates,
            "demand": [
                10,
                12,
                8,
                15,
                11,
                9,
                13,
                14,
                10,
                16,
                12,
                11,
                15,
                13,
            ],
        }
    )

    features_df = create_features(demand_df)

    training_data = prepare_training_data(features_df)

    model = train_model(training_data)

    result = forecast_future_demand(
        model,
        demand_df,
        30,
    )

    assert len(result) == 30

    assert "date" in result.columns
    assert "predicted_demand" in result.columns

    assert result["date"].is_monotonic_increasing

    assert (result["predicted_demand"] >= 0).all()
