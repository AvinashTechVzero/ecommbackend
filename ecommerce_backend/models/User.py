from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ecommerce_backend.models.common import Base
from ecommerce_backend.models import Event

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    country = Column(String)

    events = relationship("Event", back_populates="owner")
    cart = relationship("Cart", back_populates="User")
    #order_user = relationship("Order", back_populates="order_user")