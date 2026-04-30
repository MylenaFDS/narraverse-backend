from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.manager import manager
from app.core.security import get_current_user_ws

router = APIRouter()


@router.websocket("/ws/notifications")
async def notifications_ws(websocket: WebSocket):

    user = None

    try:
        token = websocket.query_params.get("token")

        if not token:
            await websocket.close(code=1008)
            return

        user = await get_current_user_ws(websocket, token)

        if not user:
            await websocket.close(code=1008)
            return

        # ✅ aceita só depois de validar
        await websocket.accept()

        await manager.connect_user(websocket, user.id)

        print(f"🔔 WS notifications conectado | user {user.id}")

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        print("🔌 WS notifications desconectado")

    except Exception as e:
        print("🔥 ERRO WS NOTIFICATIONS:", e)

    finally:
        if user:
            manager.disconnect_user(websocket, user.id)