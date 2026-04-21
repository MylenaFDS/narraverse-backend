import json
from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # 1 sala por RPG
        self.rooms: Dict[int, List[WebSocket]] = {}

        # conexões por usuário
        self.user_connections: Dict[int, List[WebSocket]] = {}

    # ===============================
    # CONNECT
    # ===============================
    async def connect(self, websocket: WebSocket, rpg_id: int, user_id: int):
        await websocket.accept()

        self.rooms.setdefault(rpg_id, []).append(websocket)
        self.user_connections.setdefault(user_id, []).append(websocket)

    # ===============================
    # DISCONNECT
    # ===============================
    def disconnect(self, websocket: WebSocket, rpg_id: int, user_id: int):
        if rpg_id in self.rooms and websocket in self.rooms[rpg_id]:
            self.rooms[rpg_id].remove(websocket)

        if user_id in self.user_connections and websocket in self.user_connections[user_id]:
            self.user_connections[user_id].remove(websocket)

    # ===============================
    # BROADCAST
    # ===============================
    async def broadcast(self, rpg_id: int, message: dict):
        for connection in self.rooms.get(rpg_id, []):
            await connection.send_text(json.dumps(message))

    # ===============================
    # 🔔 NOTIFICAÇÃO
    # ===============================
    async def send_to_user(self, user_id: int, message: dict):
        for connection in self.user_connections.get(user_id, []):
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()
