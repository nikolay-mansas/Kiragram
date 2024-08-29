from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from database import Base


user_chat_association = Table(
    'user_chat_association',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('chat_id', ForeignKey('chats.id'), primary_key=True)
)

read_messages_association = Table(
    'read_messages_association',
    Base.metadata,
    Column('message_id', ForeignKey('messages.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(32), unique=True, nullable=False)
    name = Column(String(32), nullable=False)

    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chats = relationship("Chat", secondary=user_chat_association, back_populates="users", lazy="selectin")
    messages = relationship("Message", back_populates="sender", lazy="selectin")
    read_messages = relationship("Message", secondary=read_messages_association, back_populates="read_by_users", lazy="selectin")


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(128), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", secondary=user_chat_association, back_populates="chats", lazy="selectin")
    messages = relationship("Message", back_populates="chat", lazy="selectin")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)

    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)

    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    content = Column(Text(2048), nullable=False)

    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="messages", lazy="selectin")
    sender = relationship("User", back_populates="messages", lazy="selectin")
    read_by_users = relationship("User", secondary=read_messages_association, back_populates="read_messages", lazy="selectin")
