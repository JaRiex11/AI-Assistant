from datetime import datetime, timezone


JOBS: dict[str, dict] = {}


def create_job(job_id: str) -> dict:
    job = {
        "id": job_id,
        "status": "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    JOBS[job_id] = job
    return job


def set_done(job_id: str, digest_id: str) -> None:
    if job_id in JOBS:
        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["digest_id"] = digest_id


def set_error(job_id: str, error: str) -> None:
    if job_id in JOBS:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error"] = error


def get_job(job_id: str) -> dict | None:
    return JOBS.get(job_id)