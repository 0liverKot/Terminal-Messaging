from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.orm import Session
from server.db.database import get_db
from server.db.models import RequestsModel


router = APIRouter(prefix="/requests", tags=["requests"])

class Requests(BaseModel):
    sender_name: str
    recipient_name: str


@router.get("/get_by_user/{username}")
async def get_users_requests(username: str, db: Session = Depends(get_db)):
    result = db.execute(Select(RequestsModel.sender_name).where(RequestsModel.recipient_name == username))
    requests = result.scalars().all()

    return requests


@router.get("/get_sent/{username}")
async def get_users_requests_sent(username: str, db: Session = Depends(get_db)):
    result = db.execute(Select(RequestsModel.recipient_name).where(RequestsModel.sender_name == username))
    requests = result.scalars().all()

    return requests


@router.post("/create/{sender_name}/{recipient_name}")
async def create_friend_request(sender_name: str, recipient_name: str, db: Session = Depends(get_db)):
    db_request = RequestsModel(sender_name=sender_name, recipient_name=recipient_name)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)


@router.delete("/delete/{sender_name}/{recipient_name}")
async def delete_request(sender_name: str, recipient_name: str, db: Session = Depends(get_db)):
    result = db.execute(Select(RequestsModel).where(RequestsModel.recipient_name == recipient_name and RequestsModel.sender_name == sender_name)).scalars().first()
    if result is None:
        raise HTTPException(status_code=404, detail="friend request not found")
    
    db.delete(result)
    db.commit()
