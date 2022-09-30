from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field


class EventBase(BaseModel):
    event: str
    description: Union[str, None] = None


class EventCreate(EventBase):
    pass
    event: str


class Event(EventBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
