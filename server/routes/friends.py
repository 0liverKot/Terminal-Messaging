from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Select
from server.db.database import get_db
from server.db.models import FriendsModel

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

@router.post("/create")
async def create_friendship(friend: Friends, db: Session = Depends(get_db)):
    db_friend = FriendsModel(user_name=friend.user_name, friend_name=friend.friend_name, conversation_id=None)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)

    # another entry with names the other way around
    # if user1 has friend user2 then user2 also has friend user1, must be stored
    db_friend = FriendsModel(user_name=friend.friend_name, friend_name=friend.user_name)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)