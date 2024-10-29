from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.product import ProductService
from app.schemas.users import ProductCreationReq, ProductResp
from app.database.postgres import get_session

router = APIRouter(prefix="/products", tags=["products"])

class ProductController:
    def __init__(self):
        self.service = ProductService()
    
    @router.post("/", response_model=ProductResp)
    async def create_product(
        self,
        product: ProductCreationReq,
        session: AsyncSession = Depends(get_session)
    ):
        return await self.service.create_product(session, product)

    @router.get("/{product_id}", response_model=ProductResp)
    async def get_product(
        self,
        product_id: int,
        session: AsyncSession = Depends(get_session)
    ):
        return await self.service.get_product(session, product_id)

product_controller = ProductController() 