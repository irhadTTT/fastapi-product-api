import enum


class StockMovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
