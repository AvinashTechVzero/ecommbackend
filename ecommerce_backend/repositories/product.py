from ecommerce_backend.models import Product
from ecommerce_backend.schemas import product
from sqlalchemy.orm import Session

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product.Product).offset(skip).limit(limit).all()

def create_user_product(db: Session, product: product.ProductCreate):
    db_product = Product.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product.Product).filter(Product.Product.id == product_id).first()