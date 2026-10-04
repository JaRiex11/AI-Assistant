import asyncio

from backend import jobs, storage
from src.utils.logger import log_event


STAGES = ["collecting", "dedup", "relevance", "classify", "export"]


async def run_pipeline(job_id: str, params: dict) -> None:
    """
    Запускает пайплайн агента и кладёт результат в storage.DIGESTS.
    
    Пока — заглушка. Реальный вызов пайплайна добавится позже,
    после того как HTTP-часть будет проверена.
    """
    try:
        log_event({
            "stage": "api",
            "action": "pipeline_started",
            "job_id": job_id,
            "query": params.get("query"),
        })

        # === ИМИТАЦИЯ ПАЙПЛАЙНА ===
        for stage in STAGES:
            jobs.set_stage(job_id, stage)
            await asyncio.sleep(2)   # имитация работы
        # === /ИМИТАЦИЯ ===

        preview = (
            f"# Дайджест: {params.get('query')}\n\n"
            f"Профиль: {params.get('profileId') or 'по умолчанию'}\n\n"
            f"(здесь будет результат реальной генерации)"
        )

        storage.DIGESTS[job_id] = {
            "id": job_id,
            "status": "done",
            "query": params.get("query"),
            "model": params.get("model"),
            "period": params.get("period"),
            "profileId": params.get("profileId"),
            "preview": preview,
            "articlesCount": 0,
            "sources": [],
        }

        jobs.set_done(job_id)
        log_event({
            "stage": "api",
            "action": "pipeline_finished",
            "job_id": job_id,
        })

    except Exception as e:
        jobs.set_error(job_id, str(e))
        log_event({
            "stage": "api",
            "action": "pipeline_error",
            "job_id": job_id,
            "error": str(e),
        })