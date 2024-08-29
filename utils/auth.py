from datetime import datetime, timedelta, timezone
from time import time

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from config import JWT_KEY
from database import session_maker
from models.user import User
from service.user import UserService


class JWTBearer(HTTPBearer):
    def __init__(self):
        super().__init__()

    async def __call__(self, request: Request) -> User:
        token = request.cookies.get("token", "")

        if token:
            token_data = await self._decode_jwt(token)

            if token_data is None:
                request.cookies["token"] = ""

                raise HTTPException(status_code=403)
            
            return token_data

        raise HTTPException(status_code=403)
    
    async def _decode_jwt(self, jwt_token: str) -> dict | None:
        try:
            token_data = jwt.decode(jwt_token, JWT_KEY, "HS512")
            
            if time() - token_data["exp"] > 3600:
                return None
            
            async with session_maker() as session:
                data = await UserService(session).get_user(username=token_data.get("username", ""))

            if data[0] == 200:
                return data[1]
            
            raise HTTPException(status_code=data[0], detail=data[1])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        

def generate_jwt_token(**kwargs) -> str:
    """
    {
        "username": str
    }
    """
    payload = kwargs.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    payload["exp"] = expire

    return jwt.encode(payload, JWT_KEY, "HS512")


