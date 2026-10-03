# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="ИТ/ИБ Дайджест API",
    version="0.1",
    description="Бэкенд для ассистента, собирающего тематические дайджесты публикаций",
)

# CORS — без него фронт не сможет обратиться к бэку
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # для MVP разрешаем всем
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Роут: проверка живости ----
@app.get("/api/health")
async def health():
    return {"ok": True, "version": "0.1"}