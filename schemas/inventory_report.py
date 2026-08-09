from pydantic import BaseModel


class InventoryReportResponse(BaseModel):
    total_products: int
    total_stock_units: int
    low_stock_products: int
    out_of_stock_products: int
    inventory_value: int
