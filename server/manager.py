from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []


    def get_id(self, websocket: WebSocket):
        items = str(websocket.url).split("/")
        id = items[len(items) - 1]
        return id


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)


    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        

    async def send_personal_message(self, message: str, client_id: int, websocket: WebSocket):

        for connection in self.active_connections:
            if self.get_id(websocket) != client_id:
                await connection.send_text(message)


    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()