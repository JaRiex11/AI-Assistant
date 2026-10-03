import asyncio

from backend import storage, jobs
from src.utils.logger import log_event


async def run_pipeline(job_id: str, params: dict) -> None:
    """
    Запускает пайплайн агента и кладёт результат в storage.DIGESTS.
    Пока — заглушка. Позже здесь будет вызов Collector → Normalizer → ...
    """
    try:
        log_event({
            "stage": "api",
            "action": "pipeline_started",
            "job_id": job_id,
            "query": params.get("query"),
        })

        # === ЗАГЛУШКА ===
        # Когда пайплайн будет готов — заменить этот блок на реальный вызов.
        await asyncio.sleep(2)  # имитация работы
        preview = f"# Дайджест: {params.get('query')}\n\n(здесь будет результат генерации)"
        # === /ЗАГЛУШКА ===

        digest_id = job_id
        storage.DIGESTS[digest_id] = {
            "id": digest_id,
            "status": "done",
            "query": params.get("query"),
            "model": params.get("model"),
            "period": params.get("period"),
            "profileId": params.get("profileId"),
            "sourceIds": params.get("sourceIds", []),
            "preview": preview,
            "articlesCount": 0,
            "sources": [],
        }

        jobs.set_done(job_id, digest_id)
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