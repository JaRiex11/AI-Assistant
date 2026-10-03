from fastapi import APIRouter
from backend import storage


router = APIRouter(prefix="/api", tags=["profiles"])


@router.get("/profiles")
async def list_profiles():
    return storage.PROFILES


@router.post("/profiles")
async def create_profile(profile: dict):
    profile["id"] = f"p{len(storage.PROFILES) + 1}"
    storage.PROFILES.append(profile)
    return profile


@router.put("/profiles/{profile_id}")
async def update_profile(profile_id: str, profile: dict):
    for p in storage.PROFILES:
        if p.get("id") == profile_id:
            p.update(profile)
            return p
    return profile


@router.delete("/profiles/{profile_id}")
async def delete_profile(profile_id: str):
    storage.PROFILES[:] = [p for p in storage.PROFILES if p.get("id") != profile_id]
    return {"ok": True}