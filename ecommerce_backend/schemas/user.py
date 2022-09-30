from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str



class User(BaseModel):
    email: str
    password: str
    name: str
    age: int
    country: str


class UserCreate(UserBase):
    password: str
    name: str
    age: int
    gender: str
    country: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True



class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    

class UserOut(BaseModel):
    id: UUID
    email: str
