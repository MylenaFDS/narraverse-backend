from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websockets.manager import manager
from app.core.security import get_current_user_ws # vamos ajustar se precisar

router = APIRouter()


@router.websocket("/ws/notifications")
async def notifications_ws(websocket: WebSocket):
    user = await get_current_user_ws(websocket)

    await manager.connect_user(websocket, user.id)

    try:
        while True:
            await websocket.receive_text() # mantém conexão viva
    except WebSocketDisconnect:
        manager.disconnect_user(websocket, user.id)
