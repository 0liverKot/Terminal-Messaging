from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from server.manager import manager

class Room:
    room_name: str
    websocket: WebSocket
    connections: int

    def __init__(self, websocket: WebSocket, room_name: str):
        self.websocket = websocket
        self.connections = 1
        self.room_name = room_name

    def add_connection(self):
        self.connections += 1

    def remove_connection(self):
        self.connections -= 1    


router = APIRouter(tags=["websockets"])
rooms: dict[str, Room] = {}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # first message is the room name
    room_name = await websocket.receive_text()

    if room_name not in rooms:
        rooms[room_name] = Room(websocket, room_name)
    else: 
        rooms[room_name].add_connection()

    room = rooms[room_name]


    try: 
        while True:
            pass
    except WebSocketDisconnect:
        if room.connections == 2:
            room.remove_connection()
            print("user has left the room")
        else:
            del rooms[room_name]
            del room
            print("room disconnected")