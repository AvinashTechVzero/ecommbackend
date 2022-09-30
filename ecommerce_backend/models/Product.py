from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ecommerce_backend.models.common import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)
    cart = relationship("Cart", back_populates="cart")
   

