from uuid import uuid4

from fastapi import APIRouter, HTTPException

from backend import storage
from backend.storage import _normalize_source_for_ui


router = APIRouter(prefix="/api", tags=["sources"])


@router.get("/sources")
async def list_sources():
    return storage.SOURCES


@router.post("/sources")
async def create_source(source: dict):
    if not source.get("id"):
        source["id"] = f"s-{uuid4().hex[:8]}"
    source.setdefault("active", True)
    source.setdefault("type", "rss")

    source = _normalize_source_for_ui(source)
    storage.SOURCES.append(source)
    storage.save_sources()
    return source


@router.put("/sources/{source_id}")
async def update_source(source_id: str, patch: dict):
    for i, s in enumerate(storage.SOURCES):
        if s.get("id") == source_id:
            merged = {**s, **patch}
            storage.SOURCES[i] = merged
            storage.save_sources()
            return merged
    raise HTTPException(status_code=404, detail="Источник не найден")


@router.delete("/sources/{source_id}")
async def delete_source(source_id: str):
    before = len(storage.SOURCES)
    storage.SOURCES[:] = [s for s in storage.SOURCES if s.get("id") != source_id]
    if len(storage.SOURCES) == before:
        raise HTTPException(status_code=404, detail="Источник не найден")
    storage.save_sources()
    return {"ok": True}


@router.post("/sources/{source_id}/refresh")
async def refresh_source(source_id: str):
    for s in storage.SOURCES:
        if s.get("id") == source_id:
            s["lastFetch"] = "только что"
            s["status"] = "ok"
            storage.save_sources()
            return {
                "status": "ok",
                "articlesPerDay": s.get("articlesPerDay", 0),
                "lastFetch": "только что",
            }
    raise HTTPException(status_code=404, detail="Источник не найден")


@router.post("/sources/refresh-all")
async def refresh_all():
    for s in storage.SOURCES:
        s["lastFetch"] = "только что"
        s["status"] = "ok"
    storage.save_sources()
    active = len([s for s in storage.SOURCES if s.get("active")])
    return {"ok": True, "updated": active}