import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, prospection_id: str, websocket: WebSocket):
        await websocket.accept()
        if prospection_id not in self.active_connections:
            self.active_connections[prospection_id] = []
        self.active_connections[prospection_id].append(websocket)

    def disconnect(self, prospection_id: str, websocket: WebSocket):
        if prospection_id in self.active_connections:
            self.active_connections[prospection_id].remove(websocket)
            if not self.active_connections[prospection_id]:
                del self.active_connections[prospection_id]

    async def broadcast(self, prospection_id: str, message: dict):
        if prospection_id in self.active_connections:
            for connection in self.active_connections[prospection_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass


manager = ConnectionManager()
