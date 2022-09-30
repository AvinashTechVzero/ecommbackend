from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ecommerce_backend.models.common import Base
from ecommerce_backend.models import Cart


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    products= Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Integer)
    # User = relationship("User", back_populates="cart")
    # cart = relationship("Product", back_populates="cart")
    #order = relationship("Cart", back_populates="order")
    #order_user = relationship("User", back_populates="order_user")