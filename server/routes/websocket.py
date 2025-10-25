from fastapi import APIRouter, WebSocket
from server.manager import manager

router = APIRouter(tags=["websockets"])

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    
    await manager.connect(websocket)

    try:
        while True:
            message = await websocket.receive_text()
            await manager.send_personal_message(message, client_id, websocket)
    
    except Exception:
        manager.disconnect(websocket)
