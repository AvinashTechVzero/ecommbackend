from ecommerce_backend.models import User,Cart,Event,Product,Order
from ecommerce_backend.models.common import get_db,SessionLocal,Base,engine
Base.metadata.create_all(engine)