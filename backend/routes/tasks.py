import asyncio
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from backend import jobs, storage, runner


router = APIRouter(prefix="/api", tags=["tasks"])


class GenerateRequest(BaseModel):
    query: str
    type: str = "daily"
    model: str = "gpt-oss-cloud"
    period: int = 7
    profileId: str | None = None
    sourceIds: list[str] = []


@router.post("/generate")
async def generate(req: GenerateRequest):
    """Запускает генерацию дайджеста, сразу возвращает job_id."""
    job_id = str(uuid4())
    jobs.create_job(job_id)

    if req.type == "monthly":
        asyncio.create_task(
            runner.run_monthly_pipeline(job_id, req.model_dump())
        )
    else:
        asyncio.create_task(
            runner.run_pipeline(job_id, req.model_dump())
        )

    return {"id": job_id, "status": "running"}


@router.get("/tasks/{job_id}")
async def get_task(job_id: str):
    """Возвращает статус задачи: running / done / error + текущий этап."""
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return job


@router.get("/tasks/{job_id}/result")
async def get_result(job_id: str):
    """Возвращает готовый дайджест по id задачи."""
    digest = storage.DIGESTS.get(job_id)
    if not digest:
        raise HTTPException(status_code=404, detail="Дайджест не готов")
    return digest


@router.get("/tasks/{job_id}/download")
async def download(job_id: str, format: str = "md"):
    """Отдаёт Markdown-файл для скачивания."""
    digest = storage.DIGESTS.get(job_id)
    if not digest:
        raise HTTPException(status_code=404, detail="Дайджест не готов")

    content = digest.get("preview", "")
    return Response(
        content=content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="digest-{job_id}.md"',
        },
    )