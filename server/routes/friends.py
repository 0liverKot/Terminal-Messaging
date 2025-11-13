from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Select
from server.db.database import get_db
from server.db.models import FriendsModel, ConversationModel
import server.routes.conversations as conversations
import json 

router = APIRouter(prefix="/friends", tags=["friends"])

class Friends(BaseModel):
    user_name: str
    friend_name: str
    conversation_id: int | None = None


@router.get("/get_by_user/{username}")
async def get_users_friends(username: str, db: Session = Depends(get_db)):
    result = db.execute(Select(FriendsModel.friend_name).where(FriendsModel.user_name == username))
    friends = result.scalars().all()

    return friends


@router.get("/get_friendship/{friend_name}/{username}")
async def get_friendship(username: str, friend_name: str, db: Session = Depends(get_db)):
    result = db.execute(Select(FriendsModel).where((FriendsModel.user_name == username) & (FriendsModel.friend_name == friend_name)))
    friendship: Optional[Friends] = result.scalars().first()

    if friendship is None:
        raise HTTPException(status_code=404, detail=f"friend: {friend_name} not found")

    return friendship


@router.post("/create/{user_name}/{friend_name}")
async def create_friendship(user_name: str, friend_name: str, db: Session = Depends(get_db)):
    db_friend = FriendsModel(user_name=user_name, friend_name=friend_name, conversation_id=None)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)

    # another entry with names the other way around
    # if user1 has friend user2 then user2 also has friend user1, must be stored
    db_friend = FriendsModel(user_name=friend_name, friend_name=user_name)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)


@router.post("/create/conversation")
async def create_conversation_friends(friendship: Friends, db: Session = Depends(get_db)):
    user1 = friendship.user_name
    user2 = friendship.friend_name
    conversation_id = friendship.conversation_id

    new_conversation_id = db.query(ConversationModel).count()
    messages = [{}]
    conversation = conversations.Conversation(id=new_conversation_id, messages=messages)
    await conversations.create_conversation(conversation, db=db)

    # update the conversation_id for each friendship entity
    await update_conversation_id(Friends(
        user_name=user1, 
        friend_name=user2, 
        conversation_id=conversation_id), new_conversation_id, db=db)
    
    await update_conversation_id(Friends(
        user_name=user2, 
        friend_name=user1, 
        conversation_id=conversation_id), new_conversation_id, db=db)
    
    
@router.put("/update/conversation_id")
async def update_conversation_id(friendship: Friends, id: int, db: Session = Depends(get_db)):
    result = db.execute(Select(FriendsModel).where(
        (FriendsModel.user_name == friendship.user_name) & 
        (FriendsModel.friend_name == friendship.friend_name)))
    
    db_friendship = result.scalars().first()

    if db_friendship is None:
        return 

    db_friendship.conversation_id = id
    db.commit()