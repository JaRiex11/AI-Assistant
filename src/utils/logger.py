# src/utils/logger.py
import json
import os
from datetime import datetime, timezone
from pathlib import Path


LOG_PATH = Path("data/pipeline.jsonl")

def log_event(event: dict, path: Path | None = None, verbose: bool = False) -> None:
    target = path or LOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **event,
    }

    try:
        with target.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass

    if verbose:
        print(f"[{record['stage']}] {record['action']}", {
            k: v for k, v in record.items() if k not in ("ts", "stage", "action")
        })