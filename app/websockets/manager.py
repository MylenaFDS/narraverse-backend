import json
from typing import Dict, List, Literal
from fastapi import WebSocket


# 🔥 Tipagem dos canais válidos
RoomType = Literal[
    "turns",
    "chat",
    "fichas",
    "enciclopedia",
    "anotacoes"
]


class ConnectionManager:
    def __init__(self):
        # rpg_id -> room -> lista de conexões
        self.rooms: Dict[int, Dict[RoomType, List[WebSocket]]] = {}

        # user_id -> conexões (notificações globais)
        self.user_connections: Dict[int, List[WebSocket]] = {}

    # ===============================
    # CONNECT
    # ===============================
    async def connect(
        self,
        websocket: WebSocket,
        rpg_id: int,
        user_id: int,
        room: RoomType
    ):
        await websocket.accept()

        # cria estrutura do RPG se não existir
        if rpg_id not in self.rooms:
            self.rooms[rpg_id] = {
                "turns": [],
                "chat": [],
                "fichas": [],
                "enciclopedia": [],
                "anotacoes": []
            }

        # adiciona na sala
        self.rooms[rpg_id][room].append(websocket)

        # registra usuário (para notificações)
        self.user_connections.setdefault(user_id, []).append(websocket)

        print(f"✅ Conectado | RPG {rpg_id} | Sala {room} | User {user_id}")

    # ===============================
    # DISCONNECT
    # ===============================
    def disconnect(
        self,
        websocket: WebSocket,
        rpg_id: int,
        user_id: int,
        room: RoomType
    ):
        try:
            # remove da sala
            if rpg_id in self.rooms:
                if websocket in self.rooms[rpg_id][room]:
                    self.rooms[rpg_id][room].remove(websocket)

                    # limpa sala vazia
                    if not self.rooms[rpg_id][room]:
                        self.rooms[rpg_id][room] = []

            # remove do usuário
            if user_id in self.user_connections:
                if websocket in self.user_connections[user_id]:
                    self.user_connections[user_id].remove(websocket)

                # limpa usuário sem conexões
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]

            print(f"❌ Desconectado | RPG {rpg_id} | Sala {room} | User {user_id}")

        except Exception as e:
            print("Erro ao desconectar:", e)

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
                await connection.send_text(json.dumps(message))
            except Exception:
                dead_connections.append(connection)

        # remove conexões mortas
        for conn in dead_connections:
            connections.remove(conn)

    # ===============================
    # 🔔 NOTIFICAÇÃO INDIVIDUAL
    # ===============================
    async def send_to_user(self, user_id: int, message: dict):
        connections = self.user_connections.get(user_id, [])

        dead_connections = []

        for connection in connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                dead_connections.append(connection)

        # limpa conexões mortas
        for conn in dead_connections:
            connections.remove(conn)

    # ===============================
    # DEBUG (opcional)
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
