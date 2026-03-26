from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers.prospection import router as prospection_router
from routers.lead import router as lead_router
from routers.engine import router as engine_router
from routers.export import router as export_router
from routers.settings import router as settings_router
from routers.health import router as health_router
from routers.ws_manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Prospector QC API",
    description="Sistema de prospeccao B2B com IA multi-motor",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prospection_router)
app.include_router(lead_router)
app.include_router(engine_router)
app.include_router(export_router)
app.include_router(settings_router)
app.include_router(health_router)


@app.websocket("/ws/prospection/{prospection_id}")
async def websocket_prospection(websocket: WebSocket, prospection_id: str):
    await manager.connect(prospection_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(prospection_id, websocket)


@app.get("/")
def root():
    return {
        "nome": "Prospector QC API",
        "versao": "1.0.0",
        "descricao": "Sistema de prospeccao B2B com IA multi-motor",
    }
