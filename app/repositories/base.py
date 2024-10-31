from typing import TypeVar, Generic, Type, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar('ModelType', bound=DeclarativeBase)


class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, session: AsyncSession, obj_in: ModelType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    
    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def update(self, session: AsyncSession, id: Any, **kwargs) -> Optional[ModelType]:
        query = update(self.model).where(self.model.id == id).values(**kwargs).returning(self.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

    async def delete(self, session: AsyncSession, id: Any) -> bool:
        query = delete(self.model).where(self.model.id == id)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount > 0
