from typing import Dict, List, Literal
from fastapi import WebSocket

RoomType = Literal[
    "turns",
    "chat",
    "fichas",
    "enciclopedia",
    "anotacoes"
]


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, Dict[RoomType, List[WebSocket]]] = {}
        self.user_connections: Dict[int, List[WebSocket]] = {}

    # ===============================
    # CONNECT (RPG ROOM)
    # ===============================
    async def connect(self, websocket: WebSocket, rpg_id: int, user_id: int, room: RoomType):
        if rpg_id not in self.rooms:
            self.rooms[rpg_id] = {
                "turns": [],
                "chat": [],
                "fichas": [],
                "enciclopedia": [],
                "anotacoes": []
            }

        self.rooms[rpg_id][room].append(websocket)
        self.user_connections.setdefault(user_id, []).append(websocket)

        print(f"✅ Conectado | RPG {rpg_id} | Sala {room} | User {user_id}")

    # ===============================
    # 🔔 CONNECT USER (GLOBAL)
    # ===============================
    async def connect_user(self, websocket: WebSocket, user_id: int):
        self.user_connections.setdefault(user_id, []).append(websocket)
        print(f"🔔 User WS conectado: {user_id}")

    # ===============================
    # DISCONNECT (RPG)
    # ===============================
    def disconnect(self, websocket: WebSocket, rpg_id: int, user_id: int, room: RoomType):
        try:
            if rpg_id in self.rooms:
                if websocket in self.rooms[rpg_id][room]:
                    self.rooms[rpg_id][room].remove(websocket)

            if user_id in self.user_connections:
                if websocket in self.user_connections[user_id]:
                    self.user_connections[user_id].remove(websocket)

                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]

            print(f"❌ Desconectado | RPG {rpg_id} | Sala {room} | User {user_id}")

        except Exception as e:
            print("Erro ao desconectar:", e)

    # ===============================
    # 🔔 DISCONNECT USER (GLOBAL)
    # ===============================
    def disconnect_user(self, websocket: WebSocket, user_id: int):
        if user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)

            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        print(f"🔕 User WS desconectado: {user_id}")

    # ===============================
    # 📡 BROADCAST (com limpeza)
    # ===============================
    async def broadcast(
        self,
        rpg_id: int,
        room: RoomType,
        message: dict,
        exclude_user: int | None = None
    ):
        connections = self.rooms.get(rpg_id, {}).get(room, [])
        dead = []

        for conn in connections:
            try:
                if exclude_user:
                    user_conns = self.user_connections.get(exclude_user, [])
                    if conn in user_conns:
                        continue

                await conn.send_json(message)

            except Exception:
                dead.append(conn)

        # remove conexões mortas
        for conn in dead:
            if conn in connections:
                connections.remove(conn)

    # ===============================
    # 🔔 NOTIFICAÇÃO INDIVIDUAL
    # ===============================
    async def send_to_user(self, user_id: int, message: dict):
        connections = self.user_connections.get(user_id, [])
        dead = []

        for conn in connections:
            try:
                await conn.send_json(message)
            except Exception:
                dead.append(conn)

        for conn in dead:
            if conn in connections:
                connections.remove(conn)


# instância global
manager = ConnectionManager()