import imp
from itertools import product
from re import T
from typing import List, Union
from datetime import datetime, timedelta
from urllib import response
from fastapi import Depends, FastAPI, HTTPException, Header, status 
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from uuid import uuid4
import sqlalchemy as db
from fastapi.middleware.cors import CORSMiddleware
import logging
from ecommerce_backend.services import auth as ath
from ecommerce_backend.models import get_db 
from ecommerce_backend.schemas import auth
from ecommerce_backend.schemas import user
from ecommerce_backend.schemas import product
from ecommerce_backend.schemas import event
from ecommerce_backend.schemas import cart
from ecommerce_backend.schemas import order
from ecommerce_backend.repositories import user as repo_user
from ecommerce_backend.repositories import event as repo_event
from ecommerce_backend.repositories import product as repo_product
from ecommerce_backend.repositories import cart as repo_cart
from ecommerce_backend.repositories import order as repo_order
from ecommerce_backend.models import SessionLocal
from ecommerce_backend.services import logging
from ecommerce_backend.models import User as mduser
from ecommerce_backend.models import Order
from ecommerce_backend.models import Cart 
from ecommerce_backend.services.auth import get_current_user
import json,ast
from sqlalchemy.sql.expression import func





app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     logger = logging.getLogger("uvicorn.access")
#     handler = logging.handlers.RotatingFileHandler("api.log",mode="a",maxBytes = 100*1024, backupCount = 3)
#     handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
#     logger.addHandler(handler)


origins = [
    "http://localhost",
    "https://localhost:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

# Dependency
#basic user, product creation and fetch code
# @app.on_event("startup")
# async def startup():
#     ()

@app.post("/users/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = repo_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return repo_user.create_user(db=db, user=user)


@app.get("/products/", response_model=List[product.Product])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = repo_product.get_products(db, skip=skip, limit=limit)
    return products

@app.post("/products/", response_model=product.Product)
def create_product_for_user(
     product: product.ProductCreate, db: Session = Depends(get_db)
):
    return repo_product.create_user_product(db=db, product = product)

@app.get("/products/{product_id}", response_model=product.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = repo_product.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/events", response_model=event.Event)
def create_event_for_user(
     event: event.EventCreate, db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
):
    return repo_event.create_event(db=db, event = event, owner_id=current_user.id)



@app.post("/signup", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = repo_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        user.password = ath.get_hashed_password(user.password)
        print(user.password)
        return repo_user.create_user(db=db, user=user, hashed_password=user.password)


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):  
    user_dict = db.query(mduser.User).filter(mduser.User.email ==form_data.username).first()
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if not ath.verify_password(form_data.password ,user_dict.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": ath.create_access_token(user_dict.email),
        "refresh_token":ath.create_refresh_token(user_dict.email),
    }


@app.get("/users/me", response_model=user.User)
async def read_users_me(current_user: user.User = Depends(get_current_user)):
    return current_user

@app.post("/cart", response_model=cart.Cart)
def create_cart_item_for_user(
     cart:cart.CartCreate, db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
):
    return repo_cart.create_cart_item(db=db, cart=cart, user_id=current_user.id)


@app.delete("/cart")
def delete_cart_item_for_user(
     product_id: int, db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
):
    return repo_cart.delete_cart_item(db=db,product_id=product_id, user_id=current_user.id)

@app.post("/checkout")
def checkout_cart_item_for_user(
     db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
):
     total_amount=0
     products_temp=[]
     cart_item_list_to_delete = db.query(Cart.Cart).filter(Cart.Cart.user_id == current_user.id).all()
     for records in cart_item_list_to_delete:
          cart_item_to_delete = db.query(Cart.Cart).filter(Cart.Cart.user_id == current_user.id).first()
          products = '"'+ str(cart_item_to_delete.product_id)+'":"'+str(cart_item_to_delete.product_quantity)+'"'
          if products_temp==[]:
            products_temp=products
          else:
            products_temp =  str(products)+','+ str(products_temp) 
            
          product_details = repo_product.get_product_by_id(db=db, product_id=cart_item_to_delete.product_id)
          print(product_details)
          
          total_amount = product_details.price*cart_item_to_delete.product_quantity + total_amount
          db.delete(cart_item_to_delete)
          db.commit()  
     products_temp = '{'+products_temp+'}'
     json_data = ast.literal_eval(json.dumps(products_temp))
     
     
     db_order_item =  Order.Order( products = json_data, user_id = current_user.id, total_amount=total_amount)
     db.add(db_order_item)
     db.commit()
     db.refresh(db_order_item)      
     

     return "Checkout Complete with total amount of "+str(total_amount)



@app.get("/cart", response_model=List[cart.CartResponse])
def get_cart_item_for_user(
      db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
):
    return repo_cart.get_user_cart(db=db,user_id=current_user.id)

@app.get("/orders", response_model=List[order.OrderCreate])
def get_order_item_for_user(
      db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
):      
    return repo_order.get_order(db=db,user_id=current_user.id)

@app.put("/cart")
def modify_cart_item_for_user(
     product_id: int, product_quantity: int , db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
):
    return repo_cart.update_cart_item(db=db,id=product_id,product_quantity=product_quantity)


# @app.get("/users/ordersummary", response_model=List[order_summary.OrderSummaryBase])
# def get_order_summary_for_user(
#       db: Session = Depends(get_db),current_user: user.User = Depends(get_current_user)
# ):
#     return repo_order_summary.get_order_summary(db=db,user_id=current_user.id)

# @app.post("/ordersummary", response_model=order_summary.OrderSummaryBase)
# def get_cart_item_for_user( ordersummary: order_summary.OrderSummaryCreate,
#       db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)
# ):
#     return repo_order_summary.create_user_order_summary(db=db,user_id=current_user.id,ordersummary=ordersummary)