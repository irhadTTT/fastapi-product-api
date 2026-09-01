from sqlalchemy.orm import Session

from core.exception import BadRequestException, NotFoundException
from core.logging import logger
from ml.features import (
    build_demand_dataset,
    create_features,
    forecast_future_demand,
    prepare_training_data,
)
from ml.forecasting import predict_demand, train_model
from ml.reorder import calculate_reorder_quantity, calculate_safety_stock
from repositories import (
    product_repository,
    stock_movement_repository,
)
from schemas.forecast import (
    DemandForecastItem,
    DemandForecastResponse,
    ReorderRecommendationResponse,
)


class ForecastService:
    @staticmethod
    async def get_product_demand_history(
        db: Session,
        product_id: int,
    ):
        product = product_repository.get_by_id(db, product_id)

        if not product:
            logger.warning(
                "Product not found product_id=%s",
                product_id,
            )
            raise NotFoundException("Product not found")

        movements = stock_movement_repository.get_out_movements_by_product_id(
            db,
            product_id,
        )

        demand_df = build_demand_dataset(movements)

        logger.info(
            "Demand dataset built product_id=%s days=%s",
            product_id,
            len(demand_df),
        )

        return demand_df

    @staticmethod
    def forecast_product_demand(
        db: Session,
        product_id: int,
    ) -> DemandForecastResponse:

        product = product_repository.get_by_id(db, product_id)

        if not product:
            raise NotFoundException("Product not found")

        movements = stock_movement_repository.get_by_product_id(
            db,
            product_id,
        )

        demand_df = build_demand_dataset(movements)

        if len(demand_df) < 7:
            raise BadRequestException("At least 7 days of demand history are required.")

        features_df = create_features(demand_df)

        training_data = prepare_training_data(features_df)

        model = train_model(training_data)

        predictions_df = forecast_future_demand(
            model,
            demand_df,
            days=30,
        )

        predictions = [
            DemandForecastItem(
                date=row["date"].date(),
                predicted_demand=float(row["predicted_demand"]),
            )
            for _, row in predictions_df.iterrows()
        ]

        total_predicted_demand = sum(
            prediction.predicted_demand for prediction in predictions
        )

        return DemandForecastResponse(
            product_id=product_id,
            forecast_days=30,
            predictions=predictions,
            total_predicted_demand=total_predicted_demand,
        )

    @staticmethod
    def get_reorder_recommendation(
        db: Session,
        product_id: int,
    ) -> ReorderRecommendationResponse:

        product = product_repository.get_by_id(db, product_id)

        if not product:
            raise NotFoundException("Product not found")

        movements = stock_movement_repository.get_by_product_id(
            db,
            product_id,
        )

        demand_df = build_demand_dataset(movements)

        if len(demand_df) < 7:
            raise BadRequestException("At least 7 days of demand history are required.")

        features_df = create_features(demand_df)

        training_data = prepare_training_data(features_df)

        model = train_model(training_data)

        predictions_df = forecast_future_demand(
            model,
            demand_df,
            days=30,
        )

        forecasted_demand = predictions_df["predicted_demand"].sum()

        safety_stock = calculate_safety_stock(
            demand_df["demand"],
        )

        recommended_reorder = calculate_reorder_quantity(
            product.stock_quantity,
            forecasted_demand,
            safety_stock,
        )

        return ReorderRecommendationResponse(
            product_id=product_id,
            current_stock=product.stock_quantity,
            forecasted_demand=float(forecasted_demand),
            safety_stock=float(safety_stock),
            recommended_reorder=recommended_reorder,
        )
