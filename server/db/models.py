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
    user_id = Column(Integer, ForeignKey("users.id"))