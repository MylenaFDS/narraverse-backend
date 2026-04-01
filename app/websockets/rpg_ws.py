from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.manager import manager

router = APIRouter()

@router.websocket("/ws/rpg/{rpg_id}")
async def websocket_rpg(websocket: WebSocket, rpg_id: int):
    await manager.connect(websocket, rpg_id)

    try:
        while True:
            await websocket.receive_text()  # mantém conexão viva
    except WebSocketDisconnect:
        manager.disconnect(websocket, rpg_id)