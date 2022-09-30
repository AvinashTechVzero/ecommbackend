from ecommerce_backend.models import Event 
from ecommerce_backend.schemas import event
from sqlalchemy.orm import Session

def create_event(db: Session, event: event.Event, owner_id: int):
    db_event = Event.Event(**event.dict(), owner_id=owner_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event