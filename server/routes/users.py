from typing import ClassVar, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.orm import Session
from server.db.database import get_db
from server.db.models import UserModel
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"])

class Users(BaseModel):
    username: str
    password: str


async def authenticate(username, password):

    user_details: Optional[Users] = await get_user_by_username(username)

    if(user_details is None):
        raise HTTPException(status_code=401, detail="invalid username")

    if(not pwd_context.verify(password, user_details.password)): 
        raise HTTPException(status_code=401, detail="invaid password")


@router.post("/create")
async def create_user(user: Users, db: Session = Depends(get_db)):
    
    user.password = pwd_context.hash(user.password)
    db_user = UserModel(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


@router.get("/get_user/{username}")
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    result = db.execute(Select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()
    
    # returns None if user is not found
    return user