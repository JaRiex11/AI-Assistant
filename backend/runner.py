import json
from pathlib import Path
from src.pipeline.orchestrator import run_full_pipeline
from src.utils.profile import ProfileLoader
from src.utils.logger import log_event
from backend import jobs, storage
from datetime import datetime, timezone
from src.pipeline.exporter import Exporter


def resolve_model(name: str | None) -> str:
    """Возвращает имя модели или дефолт, если пусто."""
    return name or "gpt-oss:120b"

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
            llm_model=resolve_model(params.get("model")),
            cloud=params.get("cloud", True),
        )

        # Сохраняем и в output/, и в память
        exporter = Exporter()
        saved_path = exporter.save(markdown, audience=audience)
        exporter.update_index()

        meta = {
            "id": job_id,
            "status": "done",
            "type": "daily",
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
            "md_path": str(saved_path),
            "json_path": str(saved_path.with_suffix(".json")),
            "stage": "export",          # финальный этап
        }

        storage.DIGESTS[job_id] = meta
        saved_path.with_suffix(".json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

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

async def run_monthly_pipeline(job_id: str, params: dict) -> None:
    """Месячная выжимка из сохранённых дайджестов в output/."""
    from datetime import datetime, timezone
    from pathlib import Path
    from src.pipeline.monthly import MonthlyDigest
    from src.providers.ollama import OllamaProvider
    from src.utils.prompts import PromptLoader

    started_at = datetime.now(timezone.utc)
    try:
        log_event({"stage": "api", "action": "monthly_started",
                   "job_id": job_id})

        profile_id = params.get("profileId") or "management"
        # Ежедневные дайджесты всегда сохраняются с audience="tech"
        # (фронт при «Ежедневный» передаёт profileId=security → audience=tech).
        # Месячная выжимка собирается именно из них.
        source_audience = "tech"

        days = params.get("period", 30)
        model = resolve_model(params.get("model"))

        jobs.set_stage(job_id, "collecting")

        llm = OllamaProvider(
            model=model,
            config={"temperature": 0, "seed": 42},
            cloud=params.get("cloud", True),
        )
        monthly = MonthlyDigest("output")

        path = await monthly.build(
            audience=source_audience,
            llm=llm,
            loader=PromptLoader("prompts"),
            days=days,
        )

        jobs.set_stage(job_id, "export")

        if path:
            markdown = Path(path).read_text(encoding="utf-8")
        else:
            markdown = (
                "# Месячная выжимка\n\n"
                "За указанный период сохранённых дайджестов не найдено.\n\n"
                "Сначала сгенерируйте несколько ежедневных дайджестов."
            )

        meta = {
            "id": job_id,
            "status": "done",
            "type": "monthly",
            "query": params.get("query"),
            "model": model,
            "profileId": profile_id,
            "preview": markdown,
            "articlesCount": 0,
            "sources": [],
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "durationSec": (datetime.now(timezone.utc) - started_at).total_seconds(),
            "profileName": "Для руководства" if profile_id == "management" else "Для отдела ИБ",
            "profileIcon": "📊" if profile_id == "management" else "🛡️",
            "format": "md",
            "sourcesCount": 0,
            "topicsCount": 0,
            "md_path": str(path) if path else None,
            "json_path": str(Path(path).with_suffix(".json")) if path else None,
            "stage": "export",          # финальный этап
        }

        storage.DIGESTS[job_id] = meta

        if path:
            Path(path).with_suffix(".json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        jobs.set_done(job_id)
        log_event({"stage": "api", "action": "monthly_finished",
                   "job_id": job_id})

    except Exception as e:
        jobs.set_error(job_id, str(e))
        log_event({"stage": "api", "action": "monthly_error",
                   "job_id": job_id, "error": str(e)})