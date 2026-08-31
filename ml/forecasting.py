import pandas as pd
from sklearn.ensemble import RandomForestRegressor

FEATURE_COLUMNS = [
    "lag_1",
    "lag_7",
    "rolling_mean_7",
    "day_of_week",
]


def train_model(df: pd.DataFrame) -> RandomForestRegressor:
    X = df[FEATURE_COLUMNS]
    y = df["demand"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X, y)

    return model


def predict_demand(model, features: pd.DataFrame) -> float:
    prediction = model.predict(features[FEATURE_COLUMNS])

    return float(prediction[0])
