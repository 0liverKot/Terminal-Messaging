from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .db.models import Base
from .db.database import engine
from .routes import users, conversations, websocket, requests, friends
import asyncio

app = FastAPI()
router = APIRouter(tags=["websockets"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(websocket.router)
app.include_router(requests.router)
app.include_router(friends.router)

