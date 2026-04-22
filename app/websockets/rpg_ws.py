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

    # 🔒 valida sala
    if room not in VALID_ROOMS:
        await websocket.close(code=1008)
        print(f"🚫 Sala inválida: {room}")
        return

    # 🔐 autenticação
    user = await get_current_user_ws(websocket)

    # conexão
    await manager.connect(
        websocket,
        rpg_id,
        user.id,
        room # type: ignore (safe por validação acima)
    )

    try:
        while True:
            # mantém conexão viva
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(
            websocket,
            rpg_id,
            user.id,
            room # type: ignore
        )

    except Exception as e:
        print("🔥 Erro no WS:", e)
        manager.disconnect(
            websocket,
            rpg_id,
            user.id,
            room # type: ignore
        )


print("🔥 WebSocket carregado com multi-salas")

