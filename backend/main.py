from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import storage
from backend.routes import health


app = FastAPI(
    title="ИТ/ИБ Дайджест API",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Загружает источники и профили из YAML при старте."""
    storage.init()


app.include_router(health.router)