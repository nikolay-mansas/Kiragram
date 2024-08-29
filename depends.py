from sqlalchemy.ext.asyncio import AsyncSession

from database import session_maker


async def get_session() -> AsyncSession:
	async with session_maker() as session:
		yield session
