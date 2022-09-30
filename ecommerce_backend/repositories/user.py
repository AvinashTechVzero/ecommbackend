from ecommerce_backend.models import User
from ecommerce_backend.schemas import user
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    return db.query(User.User).filter(User.User.id == user_id).first()
    


def get_user_by_email(db: Session, email: str):
    return db.query(User.User).filter(User.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user.UserCreate, hashed_password: str):
    fake_hashed_password = hashed_password
    db_user = User.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
