from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Select
from server.db.database import get_db
from server.db.models import ConversationModel, FriendsModel

router = APIRouter(tags=["conversations"])

class Conversation(BaseModel):
    id: int
    messages: List[Dict[str, Any]]

@router.post("/create")
async def create_conversation(conversation: Conversation, db: Session = Depends(get_db)):
    db_conversation = ConversationModel(id=conversation.id, messages=conversation.messages)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)


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

        non_empty_conversations.append({"friend": friend, "conversation": conversation})

    return non_empty_conversations