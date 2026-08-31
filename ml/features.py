import pandas as pd

from ml.forecasting import predict_demand


def build_demand_dataset(movements) -> pd.DataFrame:
    data = [
        {
            "date": movement.created_at.date(),
            "quantity": movement.quantity,
        }
        for movement in movements
    ]

    if not data:
        return pd.DataFrame(columns=["date", "demand"])

    df = pd.DataFrame(data)

    df = (
        df.groupby("date", as_index=False)["quantity"]
        .sum()
        .rename(columns={"quantity": "demand"})
    )

    df["date"] = pd.to_datetime(df["date"])
    # da napravim sve datume od najranije do najkasnije a "D" znaci napravi svaki dan tj da ne preskacem datum ako nema tad stockmovemnts
    date_range = pd.date_range(
        start=df["date"].min(),
        end=df["date"].max(),
        freq="D",
    )

    df = (
        df.set_index("date")
        .reindex(date_range, fill_value=0)
        .rename_axis("date")
        .reset_index()
    )

    df["demand"] = df["demand"].astype(int)

    return df.sort_values("date").reset_index(drop=True)


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["lag_1"] = df["demand"].shift(1)
    df["lag_7"] = df["demand"].shift(7)

    df["rolling_mean_7"] = df["demand"].shift(1).rolling(window=7).mean()

    df["day_of_week"] = df["date"].dt.dayofweek

    return df


def prepare_training_data(df: pd.DataFrame) -> pd.DataFrame:
    df = create_features(df)

    df = df.dropna()

    return df


def create_prediction_features(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) < 7:
        raise ValueError("At least 7 days of demand history are required.")

    last_date = df["date"].max()

    prediction_date = last_date + pd.Timedelta(days=1)

    last_demand = df.iloc[-1]["demand"]
    demand_7_days_ago = df.iloc[-7]["demand"]

    rolling_mean_7 = df["demand"].tail(7).mean()

    day_of_week = prediction_date.dayofweek

    return pd.DataFrame(
        [
            {
                "date": prediction_date,
                "lag_1": last_demand,
                "lag_7": demand_7_days_ago,
                "rolling_mean_7": rolling_mean_7,
                "day_of_week": day_of_week,
            }
        ]
    )


def forecast_future_demand(
    model,
    df: pd.DataFrame,
    days: int,
) -> pd.DataFrame:

    history = df.copy()
    predictions = []

    for _ in range(days):
        prediction_features = create_prediction_features(history)

        prediction = predict_demand(
            model,
            prediction_features,
        )

        prediction_date = prediction_features.iloc[0]["date"]

        predictions.append(
            {
                "date": prediction_date,
                "predicted_demand": prediction,
            }
        )

        history = pd.concat(
            [
                history,
                pd.DataFrame(
                    [
                        {
                            "date": prediction_date,
                            "demand": prediction,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    return pd.DataFrame(predictions)
