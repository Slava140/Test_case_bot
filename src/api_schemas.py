from pydantic import BaseModel, PositiveInt, Field


class BaseProduct(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: PositiveInt


class ProductWithID(BaseProduct):
    id: PositiveInt


class ProductWithoutID(BaseProduct):
    ...
