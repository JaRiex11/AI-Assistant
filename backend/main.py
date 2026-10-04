from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import storage
from backend.routes import health, tasks, sources, profiles, history


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
    storage.init()


app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(sources.router)
app.include_router(profiles.router)
app.include_router(history.router)