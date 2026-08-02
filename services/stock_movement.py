from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.exception import BadRequestException, NotFoundException
from enums.stock_movement_type import StockMovementType
from models.product import Item
from models.stock_movement import StockMovement
from models.user import User
from repositories import product_repository, stock_movement_repository
from schemas.stock_movement import StockMovementCreate


class StockMovementService:

    @staticmethod
    def create(
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

        return movement