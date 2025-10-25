from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy import Select
from sqlalchemy.orm import Session
from server.db.database import get_db
from server.db.models import RequestsModel

router = APIRouter(prefix="/requests", tags=["requests"])

class Requests(BaseModel):
    sender_id: int
    recipient_id: int


@router.get("/get_by_user/{username}")
async def get_users_requests(username: str, db: Session = Depends(get_db)):
    result = db.execute(Select(RequestsModel).where(RequestsModel.recipient_name == username))
    requests = result.scalars().all()

    return requests