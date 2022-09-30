from ecommerce_backend.models import Order
from ecommerce_backend.schemas import order
from sqlalchemy.orm import Session
import json,ast,re
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

def get_order(db: Session, user_id: int):
    order_data = db.query(Order.Order).filter(Order.Order.user_id == user_id).all()
    #order_data = "'"+str(order_data)+"'"
    #order_data = re.sub('[^a-zA-Z0-9{}:[]" \n\.]', '', order_data)
    #order_data = ast.literal_eval(json.dumps(order_data))
    #json_compatible_item_data = jsonable_encoder(order_data)
    return order_data
 




