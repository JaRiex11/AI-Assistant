import yaml
from pathlib import Path


SOURCES: list[dict] = []
PROFILES: list[dict] = []
DIGESTS: dict[str, dict] = {}
HISTORY: list[dict] = []


def load_sources() -> list[dict]:
    """Читает config/sources.yaml."""
    path = Path("config/sources.yaml")
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("sources", [])


def load_profiles() -> list[dict]:
    """Читает config/profile.yaml, превращает в список профилей."""
    path = Path("config/profile.yaml")
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    profiles = []
    for key, value in data.get("profiles", {}).items():
        profiles.append({
            "id": key,
            "name": value.get("name", key),
            "audience": value.get("audience", "tech"),
            "topics": value.get("focus_topics", []),
        })
    return profiles


def init():
    """Загружает источники и профили при старте сервера."""
    global SOURCES, PROFILES
    SOURCES = load_sources()
    PROFILES = load_profiles()