import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import init_db
from app.api.routes import documents, patients, health
from app.websockets import manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MedCore AI — Automation Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routes
app.include_router(documents.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
app.include_router(health.router, prefix="/api")

@app.on_event("startup")
def startup():
    init_db()
    logger.info("Startup complete")

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            # echo or implement ping/pong
            await manager.broadcast(room, {"type":"message","text": data})
    except Exception:
        manager.disconnect(websocket, room)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port, reload=settings.debug)
