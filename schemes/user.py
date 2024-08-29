from datetime import datetime
from pydantic import BaseModel, Field


class LogIn(BaseModel):
    username: str = Field(max_length=32)
    name: str = Field(max_length=32)

    password: str = Field(max_length=128)


class LogUp(BaseModel):
    username: str = Field(max_length=32)
    
    password: str = Field(max_length=32)


class GetUser(BaseModel):
    username: str
    name: str

    created_at: datetime

    chats: list
    messages: list
    read_messages: list
