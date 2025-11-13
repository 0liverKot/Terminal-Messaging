from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Select, Sequence
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

@router.put("/add_message")
async def add_message(conversation: Conversation, message: dict[str, str], db: Session = Depends(get_db)):

    if message["{sender}"] is None:
        return
    
    conversation.messages.append(message)
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


@router.get("/get/conversation_with",
            response_model=Conversation)
async def get_conversation_with(friendship: friends.Friends, db: Session = Depends(get_db)) -> Conversation:
    
    conversation_id = friendship.conversation_id

    result = db.execute(Select(ConversationModel).where(ConversationModel.id == conversation_id))
    conversation: Optional[Conversation] = result.scalars().first()

    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation with id: {conversation_id} not found")
    
    return conversation
    