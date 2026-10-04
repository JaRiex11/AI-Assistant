from src.pipeline.orchestrator import run_full_pipeline
from src.utils.profile import ProfileLoader
from src.utils.logger import log_event
from backend import jobs, storage
from datetime import datetime, timezone


async def run_pipeline(job_id: str, params: dict) -> None:
    """Запускает пайплайн агента и кладёт результат в storage.DIGESTS."""
    try:
        started_at = datetime.now(timezone.utc)

        log_event({
            "stage": "api",
            "action": "pipeline_started",
            "job_id": job_id,
            "query": params.get("query"),
        })

        # Определяем аудиторию по profileId из запроса
        profile_id = params.get("profileId") or "security"
        audience = "tech" if profile_id == "security" else "exec"

        # Колбэк: на каждом этапе пишем stage в задачу
        def on_stage(stage_name: str) -> None:
            jobs.set_stage(job_id, stage_name)

        markdown, stats = await run_full_pipeline(
            audience=audience,
            progress_callback=on_stage,
        )

        storage.DIGESTS[job_id] = {
            "id": job_id,
            "status": "done",
            "query": params.get("query"),
            "model": params.get("model"),
            "profileId": profile_id,
            "preview": markdown,
            "articlesCount": stats.final,
            "sources": [],
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "durationSec": (datetime.now(timezone.utc) - started_at).total_seconds(),
            "profileName": "Для отдела ИБ" if profile_id == "security" else "Для руководства",
            "profileIcon": "🛡️" if profile_id == "security" else "📊",
            "format": "md",
            "sourcesCount": stats.sources_count,
            "topicsCount": 0,
        }

        jobs.set_done(job_id)
        log_event({
            "stage": "api",
            "action": "pipeline_finished",
            "job_id": job_id,
            "final": stats.final,
        })

    except Exception as e:
        jobs.set_error(job_id, str(e))
        log_event({
            "stage": "api",
            "action": "pipeline_error",
            "job_id": job_id,
            "error": str(e),
        })