from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.orm import Session
from server.db.database import get_db, ROOT_URL
from server.db.models import UserModel
from passlib.context import CryptContext
import requests

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"])


class Users(BaseModel):
    username: str
    password: str


def authenticate(username, password):

    response = requests.get(f"{ROOT_URL}users/get_user/{username}").json()

    if(response is None):
        return "Invalid Username"

    if(not pwd_context.verify(password, response["password"])): 
        return "Invalid Password"

    return "success"


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
    user: Optional[Users] = result.scalars().first()

    return user