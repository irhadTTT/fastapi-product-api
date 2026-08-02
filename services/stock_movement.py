from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.exception import BadRequestException, NotFoundException
from enums.stock_movement_type import StockMovementType
from models.product import Item
from models.stock_movement import StockMovement
from models.user import User
from repositories import product_repository, stock_movement_repository
from schemas.stock_movement import (
    StockMovementCreate,
    StockMovementResponse
)
from services.cache_service import (
    get_cache, 
    set_cache, 
    delete_cache_pattern
)


class StockMovementService:

    @staticmethod
    async def create(
        db: Session, 
        data: StockMovementCreate, 
        current_user: User
    ) -> StockMovement:

        product = product_repository.get_by_id(db, data.product_id)

        if not product:
            raise NotFoundException("Product not found")

        if data.quantity <= 0:
            raise BadRequestException("Quantity must be greater than zero.")

        if data.type == StockMovementType.IN:
            product.stock_quantity += data.quantity

        elif data.type == StockMovementType.OUT:

            if product.stock_quantity < data.quantity:
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
        db.commit()
        db.refresh(movement)

        await delete_cache_pattern("stock_movements:*")

        return movement

    @staticmethod
    async def get_all_stock_movements(
        db: Session
    ):
        cache_key = "stock_movements:list"

        cached = await get_cache(cache_key)
        #moram ga vratiti iz SQLAlchemy objekta koji vraca baza u Pydantic objekat koji koristi fastAPi za prikaz
        if cached:
            return [
                StockMovementResponse.model_validate(movement)
                for movement in cached
        ]
        
        movements = stock_movement_repository.get_all(db)

        response = [
            StockMovementResponse.model_validate(movement)
            for movement in movements
        ]

        await set_cache(
            cache_key,
            [
                movement.model_dump(mode="json")
                for movement in response
            ],
            expire=300
        )
        return response

    @staticmethod
    async def get_stock_history_product(
        product_id: int,
        db: Session
    ):
        cache_key = f"stock_movements:product:{product_id}"

        cached = await get_cache(cache_key)

        if cached:
            if cached:
                return [
                    StockMovementResponse.model_validate(movement)
                    for movement in cached
                ]

        stock_movements = stock_movement_repository.get_by_product_id(db, product_id)

        response = [
            StockMovementResponse.model_validate(movement)
            for movement in stock_movements
        ]

        await set_cache(
            cache_key,
            [
                movement.model_dump(mode="json")
                for movement in response
            ],
            expire=300
        )
        return response

    @staticmethod
    async def get_stock_history_user(
        user_id: int,
        db: Session
    ):
        cache_key = f"stock_movements:user:{user_id}"

        cached = await get_cache(cache_key)

        if cached:
            if cached:
                return [
                    StockMovementResponse.model_validate(movement)
                    for movement in cached
                ]

        stock_movements = stock_movement_repository.get_by_user_id(db, user_id)
        
        response = [
            StockMovementResponse.model_validate(movement)
            for movement in stock_movements
        ]

        await set_cache(
            cache_key,
            [
                movement.model_dump(mode="json")
                for movement in response
            ],
            expire=300
        )
        return response