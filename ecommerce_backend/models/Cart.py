from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ecommerce_backend.models.common import Base
from ecommerce_backend.models import User

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product_quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    User = relationship("User", back_populates="cart")
    cart = relationship("Product", back_populates="cart")
    #order = relationship("Order", back_populates="order")