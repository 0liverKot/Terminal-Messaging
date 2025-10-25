from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from server.db.database import get_db
from server.db.models import ConversationModel

router = APIRouter(tags=["conversations"])

class Conversation(BaseModel):
    id: int
    messages: str
    user_id: int

@router.post("/create")
async def create_conversation(conversation: Conversation, db: Session = Depends(get_db)):
    db_conversation = ConversationModel(messages=conversation.messages, user_id=conversation.user_id)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)