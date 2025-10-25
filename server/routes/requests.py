from pydantic import BaseModel
from fastapi import APIRouter
from server.db.database import get_db
from server.db.models import RequestsModel

router = APIRouter(prefix="/requests", tags=["requests"])

class Requests(BaseModel):
    sender_id: int
    recipient_id: int