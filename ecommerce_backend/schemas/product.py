
from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    title: str
    description: Union[str, None] = None
    price: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    title: str

    class Config:
        orm_mode = True
