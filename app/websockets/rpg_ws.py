from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.manager import manager, RoomType
from app.core.security import get_current_user_ws

router = APIRouter()


VALID_ROOMS = {
    "turns",
    "chat",
    "fichas",
    "enciclopedia",
    "anotacoes"
}


@router.websocket("/ws/rpg/{rpg_id}/{room}")
async def websocket_endpoint(websocket: WebSocket, rpg_id: int, room: str):

    if room not in VALID_ROOMS:
        await websocket.close(code=1008)
        return

    token = websocket.query_params.get("token")

    user = await get_current_user_ws(websocket, token)

    await manager.connect(websocket, rpg_id, user.id, room)  # type: ignore

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, rpg_id, user.id, room)  # type: ignore

print("🔥 WebSocket carregado com multi-salas")

