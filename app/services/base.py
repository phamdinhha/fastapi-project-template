from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepo, ModelType

T = TypeVar('T', bound=ModelType)

class BaseService(Generic[T]):
    def __init__(self, repo: BaseRepo[T]):
        self.repo = repo

    async def create(self, session: AsyncSession, obj_in: T) -> T:
        return await self.repo.create(session, obj_in)

    async def get(self, session: AsyncSession, id: int) -> Optional[T]:
        return await self.repo.get(session, id)

    async def get_all(
        self, 
        session: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[T]:
        return await self.repo.get_all(session, skip=skip, limit=limit)

    async def update(
        self, 
        session: AsyncSession, 
        id: int, 
        **kwargs
    ) -> Optional[T]:
        return await self.repo.update(session, id, **kwargs)

    async def delete(self, session: AsyncSession, id: int) -> bool:
        return await self.repo.delete(session, id)
