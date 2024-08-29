from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class MainRepository:
    def __init__(self, db_session: AsyncSession, model):
        self.session = db_session
        self.model = model

    async def search_first(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)

        return await self.session.scalar(query)

    async def search_all(self, **kwargs) -> list:
        query = select(self.model).filter_by(**kwargs)
        
        results = await self.session.scalars(query)

        return results.all()
    
    async def create(self, model) -> None:
        self.session.add(model)

        await self.session.commit()

        return
    
    async def update(self, model) -> None:
        await self.session.merge(model)
        await self.session.commit()

        return
    
    async def refresh(self, model) -> None:
        await self.session.refresh(model)
        
        return
    
    async def delete_by_username(self, username: str) -> None:
        query = delete(self.model).where(self.model.username==username)
        
        await self.session.execute(query)
        await self.session.commit()

        return