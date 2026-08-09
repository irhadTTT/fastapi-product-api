from sqlalchemy import case, func
from sqlalchemy.orm import Session

from models.product import Item


def get_inventory_summary(
    db: Session,
    low_stock_threshold: int = 10,
):
    result = db.query(
        func.count(Item.id).label("total_products"),
        func.coalesce(func.sum(Item.stock_quantity), 0).label("total_stock_units"),
        func.count(case((Item.stock_quantity <= low_stock_threshold, 1))).label(
            "low_stock_products"
        ),
        func.count(case((Item.stock_quantity == 0, 1))).label("out_of_stock_products"),
        func.coalesce(
            func.sum(Item.price * Item.stock_quantity),
            0,
        ).label("inventory_value"),
    ).first()

    return {
        "total_products": result.total_products,
        "total_stock_units": result.total_stock_units,
        "low_stock_products": result.low_stock_products,
        "out_of_stock_products": result.out_of_stock_products,
        "inventory_value": result.inventory_value,
    }
