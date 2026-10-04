from fastapi import APIRouter

from backend import storage


router = APIRouter(prefix="/api", tags=["settings"])


@router.get("/settings")
async def get_settings():
    return storage.SETTINGS


@router.put("/settings")
async def update_settings(patch: dict):
    allowed = {
        "outputFormat", "defaultModel", "language", "cloud",
        "maxArticles", "groupByTopic", "addSources",
        "addSummary", "dedup",
    }
    for key, value in patch.items():
        if key in allowed:
            storage.SETTINGS[key] = value
    storage.save_settings(storage.SETTINGS)
    return storage.SETTINGS