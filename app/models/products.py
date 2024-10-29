from app.models.base import ModelBase
from sqlalchemy import Column, String, Float, JSON

class Product(ModelBase):
    __tablename__ = "products"
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    config = Column(JSON, nullable=True)
