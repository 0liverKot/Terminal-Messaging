from sqlalchemy import Column, ForeignKey, Integer, TEXT, VARCHAR
from .database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR(255))
    password = Column(VARCHAR(255))


class ConversationModel(Base):
    __tablename__ = "conversation"
    id = Column(Integer, primary_key=True, index=True)
    messages = Column(TEXT)


class FriendsModel(Base):
    __tablename__ = "friends"
    user_name = Column(VARCHAR(15), ForeignKey("users.id"), primary_key=True)
    friend_name = Column(VARCHAR(15), ForeignKey("users.id"), primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"))


class RequestsModel(Base):
    __tablename__ = "requests"
    sender_name = Column(VARCHAR(15), ForeignKey("users.id"), primary_key=True)
    recipient_name = Column(VARCHAR(15), ForeignKey("users.id"), primary_key=True)