from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float

class ProductCreationReq(ProductBase):
    pass

class ProductResp(ProductBase):
    id: int
    config: Optional[dict]
