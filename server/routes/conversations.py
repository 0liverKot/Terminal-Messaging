from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Select
from sqlalchemy.orm.attributes import flag_modified
from server.db.database import get_db, ROOT_URL
from server.db.models import ConversationModel, FriendsModel
import server.routes.friends as friends
import requests

router = APIRouter(prefix="/conversations", tags=["conversations"])

class Conversation(BaseModel):
    id: int
    messages: List[Dict[str, Any]]


@router.post("/create")
async def create_conversation(conversation: Conversation, db: Session = Depends(get_db)):
    db_conversation = ConversationModel(id=conversation.id, messages=conversation.messages)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)


@router.put("/add_message/{conversation_id}")
async def add_message(conversation_id: int, message: dict[str, str] = Body(...), db: Session = Depends(get_db)):

    result = db.execute(Select(ConversationModel).where(ConversationModel.id == conversation_id))
    conversation = result.scalars().first()

    if conversation is None: 
        return 
    
    conversation.messages.append(message)
    flag_modified(conversation, "messages")
    db.commit()



@router.get("/get/non_empty_conversations/{username}")
async def get_users_non_empty_conversations(username: str, db: Session = Depends(get_db)):
    result = db.execute(Select(FriendsModel).where(FriendsModel.user_name == username))
    friends = result.scalars().all()

    non_empty_conversations = []
    for friend in friends:
        result = db.execute(Select(ConversationModel.id).where(ConversationModel.id == friend.conversation_id))
        conversation = result.scalars().first()

        if conversation is None:
            continue 

        non_empty_conversations.append({"friend": friend.friend_name, "conversation-id": conversation})

    return non_empty_conversations


@router.get("/get/{id}")
async def get_conversation_with(id: int, db: Session = Depends(get_db)) -> Conversation:
    
    result = db.execute(Select(ConversationModel).where(ConversationModel.id == id))
    conversation: Optional[Conversation] = result.scalars().first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation with id: {conversation_id} not found")
    
    return conversation
    