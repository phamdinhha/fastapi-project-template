from app.repositories.base import BaseRepo
from app.models.products import Product
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from typing import Tuple, List


class ProductRepository(BaseRepo[Product]):
    def __init__(self):
        super().__init__(Product)

    async def get_by_name(
        self,
        session: AsyncSession,
        name: str,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Product], int]:
        search_pattern = f"%{name}%"
        query = (
            select(self.model)
            .filter(self.model.name.ilike(search_pattern))
            .offset(skip)
            .limit(limit)
        )
        count_query = select(func.count()).select_from(self.model).filter(self.model.name.ilike(search_pattern))
        result = await session.execute(query)
        total = await session.execute(count_query)
        return result.scalars().all(), total.scalar_one()