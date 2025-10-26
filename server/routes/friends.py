from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Select
from server.db.database import get_db
from server.db.models import FriendsModel

router = APIRouter(prefix="/friends", tags=["requests"])

class Friends(BaseModel):
    user_name: str
    friend_name: str
    conversation_id: str


@router.get("/get_by_user/{username}")
async def get_users_friends(username: str, db: Session = Depends(get_db)):
    result = db.execute(Select(FriendsModel).where(FriendsModel.user_name == username))
    friends = result.scalars().all()

    return friends