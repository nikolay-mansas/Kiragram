from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL

Base = declarative_base()

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def drop_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
