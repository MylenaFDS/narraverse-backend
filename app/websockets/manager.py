import json
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, rpg_id: int):
        await websocket.accept()
        self.rooms.setdefault(rpg_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, rpg_id: int):
        if rpg_id in self.rooms and websocket in self.rooms[rpg_id]:
            self.rooms[rpg_id].remove(websocket)

    async def broadcast(self, rpg_id: int, message: dict):
        for connection in self.rooms.get(rpg_id, []):
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()