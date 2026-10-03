import asyncio
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from backend import storage, jobs, pipeline_runner


router = APIRouter(prefix="/api", tags=["digest"])


class GenerateRequest(BaseModel):
    query: str
    model: str = "gpt-oss"
    period: int = 7
    profileId: str | None = None
    sourceIds: list[str] = []


@router.post("/generate")
async def generate(req: GenerateRequest):
    job_id = str(uuid4())
    jobs.create_job(job_id)
    asyncio.create_task(pipeline_runner.run_pipeline(job_id, req.model_dump()))
    return {"id": job_id, "status": "running"}


@router.get("/digests/{digest_id}")
async def get_digest(digest_id: str):
    # сначала смотрим в готовые
    if digest_id in storage.DIGESTS:
        return storage.DIGESTS[digest_id]
    # потом в задачи
    job = jobs.get_job(digest_id)
    if job:
        return job
    raise HTTPException(status_code=404, detail="Дайджест не найден")


@router.get("/digests/{digest_id}/download")
async def download_digest(digest_id: str, format: str = "md"):
    digest = storage.DIGESTS.get(digest_id)
    if not digest:
        raise HTTPException(status_code=404, detail="Дайджест не найден")

    content = digest["preview"]
    return Response(
        content=content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="digest-{digest_id}.md"',
        },
    )