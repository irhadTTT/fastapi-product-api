from enum import Enum


class SortField(str, Enum):
    price = "price"
    name = "name"
    created_at = "created_at"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class UserRole(str, Enum):
    admin = "admin"
    user = "user"