import yaml
from pathlib import Path


SOURCES: list[dict] = []
PROFILES: list[dict] = []
DIGESTS: dict[str, dict] = {}
HISTORY: list[dict] = []


def _read_yaml(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def load_sources() -> list[dict]:
    data = _read_yaml("config/sources.yaml")
    return data.get("sources", [])


def load_profiles() -> list[dict]:
    """Читает config/profile.yaml, превращает в список профилей."""
    data = _read_yaml("config/profile.yaml")
    result = []
    for key, value in (data.get("profiles") or {}).items():
        result.append({
            "id": key,
            "name": value.get("name", key),
            "audience": value.get("audience", "tech"),
            "topics": value.get("focus_topics", []),
        })
    return result


def init() -> None:
    """Загружает источники и профили при старте сервера."""
    global SOURCES, PROFILES
    SOURCES = load_sources()
    PROFILES = load_profiles()