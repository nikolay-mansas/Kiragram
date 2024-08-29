from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemes.user import LogUp, LogIn
from repositories.main import MainRepository
from bcrypt import checkpw, gensalt, hashpw
import uuid


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = MainRepository(session, User)
    
    async def login_user(self, data: LogUp) -> tuple[int, User | None]:
        user = await self.repository.search_first(username=data.username)

        if user is None:
            return 404, "User not found"

        if not checkpw(data.password.encode("utf-8"), user.password_hash.encode("utf8")):
            return 404, "Password is not correct"
        
        del user.id
        del user.password_hash
        
        return 200, user

    async def get_user(self, username: str) -> tuple[int, User | str]:
        user = await self.repository.search_first(username=username)

        if user is None:
            return 404, "User not found"
        
        del user.id
        del user.password_hash
        
        return 200, user
    
    async def delete_user(self, username: str) -> tuple[int, dict | str]:
        user = await self.repository.search_first(username=username)

        if user is None:
            return 404, "User not found"
        
        await self.repository.delete_by_username(user.username)

        return 200, {True}
    
    async def create_user(self, data: LogIn) -> tuple[int, User | str]:
        user = await self.get_user(data.username)

        if user[0] == 200:
            return 400, "User already exists"

        new_user = User(
            username=data.username,
            name=data.name,
            password_hash=hashpw(data.password.encode("utf-8"), gensalt(14)).decode("utf-8")
        )

        await self.repository.create(new_user)
        await self.repository.refresh(new_user)

        del new_user.id
        del new_user.password_hash

        return 201, new_user
    
    """async def update_task(self, pk: uuid.UUID, task: Task_s) -> tuple[int, Task_m | None]:
        old_task: Task_m | None = await self.get_task(pk)[1]

        if old_task is None:
            return 404, None
        
        old_task.emails = task.emails
        old_task.name = task.name
        old_task.short_desc = task.short_desc if task.short_desc is not None else old_task.short_desc
        old_task.desc = task.desc
        old_task.completed = task.completed if task.completed is not None else old_task.completed
        old_task.expire = task.expire if task.expire else old_task.expire

        await self.repository.update(old_task)

        return old_task"""

