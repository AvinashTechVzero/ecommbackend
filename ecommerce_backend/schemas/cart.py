from itertools import product
from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field


class CartBase(BaseModel):
    product_id: int
    product_quantity: int
    


class CartCreate(CartBase):
    pass
    

class Cart(CartBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class CartResponse(CartBase):
    id: int
    product_id: int
    product_quantity: int
    user_id: int

    class Config:
        orm_mode = True
