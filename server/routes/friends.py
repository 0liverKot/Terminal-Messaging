from pydantic import BaseModel
from fastapi import APIRouter
from server.db.database import get_db
from server.db.models import FriendsModel

router = APIRouter(prefix="/requests", tags=["requests"])

class Friends(BaseModel):
    user_id: int
    friend_id: int
    conversation_id: str