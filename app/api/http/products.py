from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.product import ProductService
from app.schemas.products import ProductCreationReq, ProductResp
from app.database.postgres import get_session


router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResp)
async def create_product(
    product: ProductCreationReq,
    session: AsyncSession = Depends(get_session),
    service: ProductService = Depends(ProductService)
):
    return await service.create_product(session, product)

@router.get("/{product_id}", response_model=ProductResp)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    service: ProductService = Depends(ProductService)
):
    return await service.get_product(session, product_id) 