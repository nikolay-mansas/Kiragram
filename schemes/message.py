import uuid

from fastapi import Query
from pydantic import BaseModel, Field
from datetime import date


class GetMessage(BaseModel):
    pk: uuid.UUID
    chat: uuid.UUID

    sender: str
    created: date

    users_received: list[str]


class GetChat(BaseModel):
    pk: uuid.UUID

    name: str

    users: list[str]


class CreateMessage(BaseModel):
    chat: uuid.UUID = Field()

    text: str = Field(max_length=2048)


class CreateChat(BaseModel):
    name: str = Field(max_length=255)

    users: list[str] = Query()
