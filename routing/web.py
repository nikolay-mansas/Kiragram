from typing import List

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from depends import get_session
from models.user import Chat, Message


router = APIRouter(prefix="/web", tags=["Web"])
