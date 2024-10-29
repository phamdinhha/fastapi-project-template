from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.models.products import Product
from app.repositories.product import ProductRepository
from app.schemas.users import ProductCreationReq, ProductResp

class ProductService(BaseService[Product]):
    def __init__(self):
        super().__init__(ProductRepository())

    async def create_product(
        self, 
        session: AsyncSession, 
        product_data: ProductCreationReq
    ) -> ProductResp:
        product = await self.create(session, product_data)
        return ProductResp.model_validate(product)

    async def get_product(
        self, 
        session: AsyncSession, 
        product_id: int
    ) -> Optional[ProductResp]:
        product = await self.get(session, product_id)
        return ProductResp.model_validate(product) if product else None

    async def search_products(
        self, 
        session: AsyncSession, 
        name: str, 
        skip: int = 0, 
        limit: int = 20
    ) -> Tuple[List[ProductResp], int]:
        products, total = await self.repo.get_by_name(
            session, 
            name, 
            skip=skip, 
            limit=limit
        )
        return [ProductResp.model_validate(p) for p in products], total

    async def list_products(
        self, 
        session: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ProductResp]:
        products = await self.get_all(session, skip=skip, limit=limit)
        return [ProductResp.model_validate(p) for p in products]

    async def update_product(
        self, 
        session: AsyncSession, 
        product_id: int, 
        product_data: dict
    ) -> Optional[ProductResp]:
        product = await self.update(session, product_id, **product_data)
        return ProductResp.model_validate(product) if product else None

    async def delete_product(
        self, 
        session: AsyncSession, 
        product_id: int
    ) -> bool:
        return await self.delete(session, product_id)
