from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.manager import manager
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

    await websocket.accept()  # ✅ ÚNICO ACCEPT

    user = None

    try:
        token = websocket.query_params.get("token")
        user = await get_current_user_ws(websocket, token)

        await manager.connect(websocket, rpg_id, user.id, room)

        print(f"✅ WS RPG conectado | user {user.id} | sala {room}")

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        print("❌ WS RPG desconectado")

    except Exception as e:
        print("🔥 ERRO WS RPG:", e)

    finally:
        if user:
            manager.disconnect(websocket, rpg_id, user.id, room)