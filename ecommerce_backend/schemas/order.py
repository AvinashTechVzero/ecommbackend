from itertools import product
from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    total_amount: int
    products: str
    
    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    pass
    

class Order(OrderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
