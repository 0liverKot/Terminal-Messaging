import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging

class Room:
    room_name: str
    websockets: list[dict[str, WebSocket]] = []
    connections: int
    users = set()

    def __init__(self, websocket: WebSocket, room_name: str, username: str):
        self.websockets.append({f"{username}": websocket})
        self.connections = 1
        self.users.add(username)
        self.room_name = room_name

    def add_connection(self, username, websocket):
        self.connections += 1
        self.users.add(username)
        self.websockets.append({f"{username}": websocket})

    def remove_connection(self, username):
        self.connections -= 1    
        self.users.remove(username)

        for socket in self.websockets:
            if list(socket.keys())[0] == username:
                self.websockets.remove(socket)


router = APIRouter(tags=["websockets"])
rooms: dict[str, Room] = {}
logger = logging.getLogger("uvicorn")

async def send_message(message, room: Room, websocket: WebSocket):
        
        sender = message["sender"]
        for socket in room.websockets:
            if list(socket.keys())[0] != sender:
                await list(socket.values())[0].send_json(message)
        

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()

    # first message is the room name
    room_name = await websocket.receive_text()

    if room_name not in rooms:
        rooms[room_name] = Room(websocket, room_name, username)
    else: 
        rooms[room_name].add_connection(username, websocket)

    room = rooms[room_name]


    try: 
        while True:
            message = await websocket.receive_json()
            await send_message(message, room, websocket)

    except WebSocketDisconnect:
        if room.connections == 2:
            room.remove_connection(username)
            print("user has left the room")
        else:
            del rooms[room_name]
            del room
            print("room disconnected")