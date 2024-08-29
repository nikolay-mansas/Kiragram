from typing import List

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from depends import get_session
from models.user import User
from schemes.user import LogIn, LogUp, GetUser 
from service.user import UserService
from utils.auth import JWTBearer, generate_jwt_token


router = APIRouter(prefix="/user", tags=["User"])



@router.get(
    "/me",
    status_code=200,
    response_model=GetUser
)
async def get_me(
    user: User = Depends(JWTBearer())
) -> JSONResponse:
    return JSONResponse(jsonable_encoder(user))


@router.post(
    "/register",
    status_code=201,
    response_model=GetUser
)
async def create_user(
    data: LogIn,

    session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    new_user = await UserService(session).create_user(data)

    response = JSONResponse(jsonable_encoder(new_user[1]), new_user[0])

    if new_user[0] == 201:
        response.set_cookie("token", generate_jwt_token(username=data.username), max_age=3600)

    return response


@router.post(
    "/login",
    status_code=200,
    response_model=str
)
async def login(
    data: LogUp,

    session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    user = await UserService(session).login_user(data)

    response = JSONResponse("true", user[0])

    if user[0] == 200:
        response.set_cookie("token", generate_jwt_token(username=data.username), max_age=3600)
        
    if user[0] == 404:
        response = JSONResponse(jsonable_encoder(user[1]), user[0])

    return response


@router.delete(
    "/delete",
    status_code=200,
    response_model=str
)
async def delete_account(
    user: User = Depends(JWTBearer()),  
    session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    account = await UserService(session).delete_user(user.username)

    response = JSONResponse(jsonable_encoder(account[1]), account[0])
    
    return response


@router.get(
    "/log-out",
    status_code=200
)
async def log_out(response: Response) -> Response:
    response.delete_cookie("token")
    response.status_code = 200  # bug resolution "reason = STATUS_PHRASES[status] KeyError: None"

    return response
