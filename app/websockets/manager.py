import json
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
    async def connect(
        self,
        websocket: WebSocket,
        rpg_id: int,
        user_id: int,
        room: RoomType
    ):
        # ❌ REMOVIDO websocket.accept()

        if rpg_id not in self.rooms:
            self.rooms[rpg_id] = {
                "turns": [],
                "chat": [],
                "fichas": [],
                "enciclopedia": [],
                "anotacoes": []
            }

        self.rooms[rpg_id][room].append(websocket)

        # registrar também no usuário
        self.user_connections.setdefault(user_id, []).append(websocket)

        print(f"✅ Conectado | RPG {rpg_id} | Sala {room} | User {user_id}")

    # ===============================
    # 🔔 CONNECT USER (GLOBAL)
    # ===============================
    async def connect_user(self, websocket: WebSocket, user_id: int):
        self.user_connections.setdefault(user_id, []).append(websocket)
        print(f"🔔 User WS conectado: {user_id}")

    # ===============================
    # DISCONNECT (RPG ROOM)
    # ===============================
    def disconnect(
        self,
        websocket: WebSocket,
        rpg_id: int,
        user_id: int,
        room: RoomType
    ):
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
    # BROADCAST (POR SALA)
    # ===============================
    async def broadcast(
        self,
        rpg_id: int,
        room: RoomType,
        message: dict
    ):
        connections = self.rooms.get(rpg_id, {}).get(room, [])

        dead_connections = []

        for connection in connections:
            try:
                await connection.send_json(message)  # 🔥 melhor que send_text
            except Exception:
                dead_connections.append(connection)

        for conn in dead_connections:
            if conn in connections:
                connections.remove(conn)

    # ===============================
    # 🔔 NOTIFICAÇÃO INDIVIDUAL
    # ===============================
    async def send_to_user(self, user_id: int, message: dict):
        connections = self.user_connections.get(user_id, [])

        dead_connections = []

        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        for conn in dead_connections:
            if conn in connections:
                connections.remove(conn)

    # ===============================
    # DEBUG
    # ===============================
    def debug(self):
        print("=== ROOMS ===")
        for rpg_id, rooms in self.rooms.items():
            for room, conns in rooms.items():
                print(f"RPG {rpg_id} | {room}: {len(conns)} conexões")

        print("=== USERS ===")
        for user_id, conns in self.user_connections.items():
            print(f"User {user_id}: {len(conns)} conexões")


# instância global
manager = ConnectionManager()