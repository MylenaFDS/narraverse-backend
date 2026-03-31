from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
from app.websockets.manager import manager

router = APIRouter()

# salas por RPG
rooms: Dict[int, List[WebSocket]] = {}

@router.websocket("/ws/rpg/{rpg_id}")
async def websocket_rpg(websocket: WebSocket, rpg_id: int):
    await manager.connect(websocket, rpg_id)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, rpg_id)
    await websocket.accept()

    if rpg_id not in rooms:
        rooms[rpg_id] = []

    rooms[rpg_id].append(websocket)

    try:
        while True:
            await websocket.receive_text()  # mantém conexão viva

    except WebSocketDisconnect:
        rooms[rpg_id].remove(websocket)