from fastapi import APIRouter

from backend import storage


router = APIRouter(prefix="/api", tags=["sources"])


@router.get("/sources")
async def list_sources():
    return storage.SOURCES


@router.post("/sources")
async def create_source(source: dict):
    source.setdefault("id", f"s{len(storage.SOURCES) + 1}")
    source.setdefault("active", True)
    storage.SOURCES.append(source)
    return source


@router.put("/sources/{source_id}")
async def update_source(source_id: str, patch: dict):
    for s in storage.SOURCES:
        if s.get("id") == source_id:
            s.update(patch)
            return s
    return {"ok": True, "id": source_id, **patch}


@router.delete("/sources/{source_id}")
async def delete_source(source_id: str):
    storage.SOURCES[:] = [s for s in storage.SOURCES if s.get("id") != source_id]
    return {"ok": True}


@router.post("/sources/{source_id}/refresh")
async def refresh_source(source_id: str):
    return {"status": "ok", "articlesPerDay": 0, "lastFetch": "только что"}


@router.post("/sources/refresh-all")
async def refresh_all():
    return {"ok": True, "updated": 0}


@router.post("/sources/import-opml")
async def import_opml():
    return {"added": 0, "skipped": 0, "sources": []}


@router.get("/sources/export-opml")
async def export_opml():
    from fastapi.responses import Response
    opml = '<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0"><body/></opml>'
    return Response(
        content=opml,
        media_type="text/xml",
        headers={"Content-Disposition": 'attachment; filename="sources.opml"'},
    )