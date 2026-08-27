from fastapi import Header, HTTPException, status
from sqlalchemy.orm import Session

from core.exception import BadRequestException, NotFoundException
from core.logging import logger
from core.metrics import stock_movements
from enums.stock_movement_type import StockMovementType
from models.idempotency_key import IdempotencyKey
from models.product import Item
from models.stock_movement import StockMovement
from models.user import User
from repositories import (
    idempotency_repository,
    product_repository,
    stock_movement_repository,
)
from schemas.stock_movement import StockMovementCreate, StockMovementResponse
from services.cache_service import delete_cache_pattern, get_cache, set_cache


class StockMovementService:
    @staticmethod
    async def create(
        db: Session, data: StockMovementCreate, current_user: User, idempotency_key: str
    ) -> StockMovement:

        existing_key = idempotency_repository.get_by_key(db, idempotency_key)

        if existing_key:
            logger.info(
                "Duplicate stock movement request ignored "
                "idempotency_key=%s user_id=%s",
                idempotency_key,
                current_user.id,
            )
            return stock_movement_repository.get_by_id(
                db, existing_key.stock_movement_id
            )

        product = product_repository.get_by_id(db, data.product_id)

        if not product:
            logger.warning(
                "Product not found product_id=%s user_id=%s",
                data.product_id,
                current_user.id,
            )
            raise NotFoundException("Product not found")

        if data.quantity <= 0:
            logger.warning(
                "Quantity must be greater than zero product_id=%s product_name=%s user_id=%s",
                data.product_id,
                product.name,
                current_user.id,
            )
            raise BadRequestException("Quantity must be greater than zero.")

        if data.type == StockMovementType.IN:
            product.stock_quantity += data.quantity

        elif data.type == StockMovementType.OUT:
            if product.stock_quantity < data.quantity:
                logger.warning(
                    "Not enough products on the stock product_id=%s product_name=%s user_id=%s",
                    data.product_id,
                    product.name,
                    current_user.id,
                )
                raise BadRequestException("Not enough products on the stock.")

            product.stock_quantity -= data.quantity

        product_repository.save_product(db, product)

        movement = StockMovement(
            product_id=product.id,
            user_id=current_user.id,
            type=data.type,
            quantity=data.quantity,
            note=data.note,
        )

        stock_movement_repository.create(db, movement)

        db.flush()

        idempotency_key = IdempotencyKey(
            key=idempotency_key, user_id=current_user.id, stock_movement_id=movement.id
        )

        db.add(idempotency_key)

        db.commit()
        db.refresh(movement)

        stock_movements.labels(type=data.type.value).inc()

        logger.info(
            "Stock movement created for product_id=%s created_by=%s",
            movement.product_id,
            current_user.id,
        )

        await delete_cache_pattern("stock_movements:*")
        await delete_cache_pattern("products:*")

        logger.debug(
            "Stock movement cache invalidated pattern=%s action=%s",
            "stock_movements:*",
            "create",
        )

        logger.debug(
            "Products cache invalidated pattern=%s action=%s", "products:*", "create"
        )

        return movement

    @staticmethod
    async def get_all_stock_movements(db: Session, page, limit):
        cache_key = f"stock_movements:list:{page}:{limit}"

        cached = await get_cache(cache_key)
        # moram ga vratiti iz SQLAlchemy objekta koji vraca baza u Pydantic objekat koji koristi fastAPi za prikaz
        if cached:
            logger.debug(
                "Stock movements fetched from cache page=%s limit=%s count=%s",
                page,
                limit,
                len(cached["movements"]),
            )
            return {
                "movements": [
                    StockMovementResponse.model_validate(movement)
                    for movement in cached["movements"]
                ],
                "page": cached["page"],
                "limit": cached["limit"],
                "total": cached["total"],
                "total_pages": cached["total_pages"],
            }

        movements, total = stock_movement_repository.get_all(db, page, limit)

        logger.info(
            "Stock movements fetched from database page=%s limit=%s count=%s",
            page,
            limit,
            len(movements),
        )

        response = [
            StockMovementResponse.model_validate(movement) for movement in movements
        ]

        total_pages = (total + limit - 1) // limit

        result = {
            "movements": response,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
        }

        await set_cache(
            cache_key,
            {
                "movements": [
                    movement.model_dump(mode="json") for movement in response
                ],
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
            },
            expire=300,
        )

        logger.debug(
            "Stock movements cache updated page=%s limit=%s count=%s",
            page,
            limit,
            len(response),
        )

        return result

    @staticmethod
    async def get_stock_history_product(product_id: int, db: Session):
        cache_key = f"stock_movements:product:{product_id}"

        cached = await get_cache(cache_key)

        if cached:
            logger.debug("Stock movements fetched from cache count=%s", len(cached))
            return [
                StockMovementResponse.model_validate(movement) for movement in cached
            ]

        stock_movements = stock_movement_repository.get_by_product_id(db, product_id)

        logger.info(
            "Stock movements fetched from database count=%s", len(stock_movements)
        )

        response = [
            StockMovementResponse.model_validate(movement)
            for movement in stock_movements
        ]

        await set_cache(
            cache_key,
            [movement.model_dump(mode="json") for movement in response],
            expire=300,
        )

        logger.debug("Stock movements cache updated count=%s", len(response))

        return response

    @staticmethod
    async def get_stock_history_user(user_id: int, db: Session):
        cache_key = f"stock_movements:user:{user_id}"

        cached = await get_cache(cache_key)

        if cached:
            logger.debug("Stock movements fetched from cache count=%s", len(cached))
            return [
                StockMovementResponse.model_validate(movement) for movement in cached
            ]

        stock_movements = stock_movement_repository.get_by_user_id(db, user_id)

        logger.info(
            "Stock movements fetched from database count=%s", len(stock_movements)
        )

        response = [
            StockMovementResponse.model_validate(movement)
            for movement in stock_movements
        ]

        await set_cache(
            cache_key,
            [movement.model_dump(mode="json") for movement in response],
            expire=300,
        )

        logger.debug("Stock movements cache updated count=%s", len(response))
        return response
