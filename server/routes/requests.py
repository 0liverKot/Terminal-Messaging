from pydantic import BaseModel
from fastapi import APIRouter, Depends
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

@router.post("/create")
async def create_friend_request(request: Requests, db: Session = Depends(get_db)):
    db_request = RequestsModel(sender_name=request.sender_name, recipient_name=request.recipient_name)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)