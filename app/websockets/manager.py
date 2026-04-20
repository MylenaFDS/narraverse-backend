import json
from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # 🔥 salas de RPG (já existe)
        self.rooms: Dict[int, List[WebSocket]] = {}

        # 🚀 NOVO: conexões por usuário
        self.user_connections: Dict[int, List[WebSocket]] = {}

    # ===============================
    # RPG (já existente)
    # ===============================
    async def connect(self, websocket: WebSocket, rpg_id: int):
        await websocket.accept()
        self.rooms.setdefault(rpg_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, rpg_id: int):
        if rpg_id in self.rooms and websocket in self.rooms[rpg_id]:
            self.rooms[rpg_id].remove(websocket)

    async def broadcast(self, rpg_id: int, message: dict):
        for connection in self.rooms.get(rpg_id, []):
            await connection.send_text(json.dumps(message))

    # ===============================
    # 🚀 USER (NOTIFICAÇÕES)
    # ===============================
    async def connect_user(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.user_connections.setdefault(user_id, []).append(websocket)

    def disconnect_user(self, websocket: WebSocket, user_id: int):
        if user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)

    async def send_to_user(self, user_id: int, message: dict):
        for connection in self.user_connections.get(user_id, []):
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()