from ecommerce_backend.models import Cart
from ecommerce_backend.models import Order
from ecommerce_backend.schemas import cart
from sqlalchemy.orm import Session
from sqlalchemy.engine import result
import sqlalchemy
from sqlalchemy import create_engine, MetaData,\
Table, Column, Numeric, Integer, VARCHAR, update, delete

def create_cart_item(db: Session, cart: cart.Cart, user_id: int):
     db_cart = Cart.Cart(**cart.dict(), user_id=user_id)
     db.add(db_cart)
     db.commit()
     db.refresh(db_cart)
     return db_cart


def delete_cart_item(db: Session, product_id:int, user_id:int ):
     cart_item_to_delete = db.query(Cart.Cart).filter(Cart.Cart.product_id == product_id).filter(Cart.Cart.user_id==user_id).first()
     db.delete(cart_item_to_delete)
     db.commit()
     return cart_item_to_delete

def cart_checkout(db: Session, id:int ):
     cart_item_list_to_delete = db.query(Cart.Cart).filter(Cart.Cart.user_id == id).all()
     for records in cart_item_list_to_delete:
          cart_item_to_delete = db.query(Cart.Cart).filter(Cart.Cart.user_id == id).first()
          # print(cart_item_to_delete.product_id)
          # db_order_item =  Order.Order(product_id=cart_item_to_delete.product_id, product_quantity=cart_item_to_delete.product_quantity, user_id = cart_item_to_delete.user_id, order_id=order_id)
          # db.add(db_order_item)
          # db.commit()
          # db.refresh(db_order_item)
          db.delete(cart_item_to_delete) 
          db.commit()
     return 

def get_user_cart(db: Session, user_id: int):
     cart_item_list = db.query(Cart.Cart).filter(Cart.Cart.user_id==user_id).all()
     return cart_item_list

def update_cart_item(db: Session, product_id:int, product_quantity: int):
     cart_item_to_update = db.query(Cart.Cart).filter(Cart.Cart.product_id == product_id).first()
     cart_item_to_update.product_quantity=product_quantity
     db.commit()
     return cart_item_to_update
