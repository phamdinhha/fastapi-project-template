from app.models.base import ModelBase
from sqlalchemy import Column, String, Float, JSON

class Product(ModelBase):
    __tablename__ = "products"
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    config = Column(JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "config": self.config,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
