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

    user = None

    try:
        # 🔐 autenticação ANTES do accept
        token = websocket.query_params.get("token")

        if not token:
            await websocket.close(code=1008)
            return

        user = await get_current_user_ws(websocket, token)

        if not user:
            await websocket.close(code=1008)
            return

        # ✅ agora aceita
        await websocket.accept()

        await manager.connect(websocket, rpg_id, user.id, room)

        print(f"✅ WS RPG conectado | user {user.id} | sala {room}")

        # 🟢 ONLINE
        await manager.broadcast(
            rpg_id,
            room,
            {
                "type": "user_online",
                "user_id": user.id,
                "username": user.username,
            },
            exclude_user=user.id,
        )

        # 🔥 LOOP CORRIGIDO
        while True:
            try:
                data = await websocket.receive_json()
                msg_type = data.get("type")

                if msg_type == "typing_start":
                    await manager.broadcast(
                        rpg_id,
                        room,
                        {
                            "type": "typing_start",
                            "username": user.username,
                        },
                        exclude_user=user.id,
                    )

                elif msg_type == "typing_stop":
                    await manager.broadcast(
                        rpg_id,
                        room,
                        {
                            "type": "typing_stop",
                            "username": user.username,
                        },
                        exclude_user=user.id,
                    )

                elif msg_type == "read_messages":
                    message_ids = data.get("message_ids", [])

                    if isinstance(message_ids, list):
                        await manager.broadcast(
                            rpg_id,
                            room,
                            {
                                "type": "message_read",
                                "message_ids": message_ids,
                                "user_id": user.id,
                            },
                            exclude_user=user.id,
                        )

            # ✅ 🔥 CORREÇÃO PRINCIPAL
            except WebSocketDisconnect:
                print(f"❌ WS RPG desconectado | user {user.id}")
                break  # 🚨 ESSENCIAL — para o loop

            # ✅ evita loop infinito com erro
            except Exception as inner_error:
                print("⚠️ erro WS mensagem:", inner_error)
                break  # 🚨 evita spam infinito

    except WebSocketDisconnect:
        print(f"❌ WS RPG desconectado (outer) | user {user.id if user else 'unknown'}")

    except Exception as e:
        print("🔥 ERRO WS RPG:", e)

    finally:
        if user:
            try:
                await manager.broadcast(
                    rpg_id,
                    room,
                    {
                        "type": "user_offline",
                        "user_id": user.id,
                        "username": user.username,
                    },
                    exclude_user=user.id,
                )
            except Exception:
                pass

            manager.disconnect(websocket, rpg_id, user.id, room)