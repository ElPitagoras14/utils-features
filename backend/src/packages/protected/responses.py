from pydantic import BaseModel

from utils.responses import SuccessResponse


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float


class ProductList(BaseModel):
    items: list[Product]
    total: int


class ProductListOut(SuccessResponse):
    payload: ProductList | None
