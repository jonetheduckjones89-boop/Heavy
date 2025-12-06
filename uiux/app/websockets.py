from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import asyncio
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        self.active_connections.setdefault(room, []).append(websocket)
        logger.debug("WS connected to %s", room)

    def disconnect(self, websocket: WebSocket, room: str):
        self.active_connections.get(room, []).remove(websocket)

    async def broadcast(self, room: str, message: dict):
        conns = list(self.active_connections.get(room, []))
        for conn in conns:
            try:
                await conn.send_json(message)
            except Exception:
                logger.exception("broadcast fail")

manager = ConnectionManager()
