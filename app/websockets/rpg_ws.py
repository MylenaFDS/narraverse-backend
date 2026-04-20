from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.manager import manager
from app.core.security import get_current_user_ws

router = APIRouter()

@router.websocket("/ws/rpg/{rpg_id}")
async def websocket_endpoint(websocket: WebSocket, rpg_id: int):
    user = await get_current_user_ws(websocket)

    await manager.connect(websocket, rpg_id)

    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket, rpg_id)
print("WS CARREGADO")