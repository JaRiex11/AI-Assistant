from fastapi import APIRouter

from backend import storage


router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history")
async def list_history(period: int | None = None, search: str | None = None):
    items = list(storage.DIGESTS.values())
    if search:
        s = search.lower()
        items = [i for i in items if s in (i.get("query") or "").lower()]
    return items


@router.delete("/history/{digest_id}")
async def delete_history(digest_id: str):
    storage.DIGESTS.pop(digest_id, None)
    return {"ok": True}


@router.delete("/history")
async def clear_history():
    storage.DIGESTS.clear()
    return {"ok": True}


@router.post("/history/{digest_id}/repeat")
async def repeat_digest(digest_id: str):
    return {"ok": True, "id": digest_id}