import yaml
import json
import re

from datetime import datetime
from pathlib import Path
from uuid import uuid4


SOURCES: list[dict] = []
PROFILES: list[dict] = []
DIGESTS: dict[str, dict] = {}
HISTORY: list[dict] = []

_MD_DAILY_RE = re.compile(
    r"^digest_(?P<audience>tech|exec)_(?P<date>\d{4}-\d{2}-\d{2})_(?P<time>\d{2}-\d{2})\.md$"
)
_MD_MONTHLY_RE = re.compile(
    r"^digest_(?P<audience>tech|exec)_monthly_(?P<month>\d{4}-\d{2})\.md$"
)

DEFAULT_SETTINGS = {
    "outputFormat": "md",
    "defaultModel": "gpt-oss:120b",
    "language": "ru",
    "cloud": True,
    "maxArticles": 25,
    "groupByTopic": True,
    "addSources": True,
    "addSummary": True,
    "dedup": True,
}

SETTINGS: dict = {}


def load_settings() -> dict:
    path = Path("data/settings.json")
    if not path.exists():
        return dict(DEFAULT_SETTINGS)
    try:
        return {**DEFAULT_SETTINGS, **json.loads(path.read_text(encoding="utf-8"))}
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict) -> None:
    path = Path("data/settings.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def _audience_meta(audience: str) -> dict:
    """Метаданные профиля по аудитории."""
    if audience == "exec":
        return {
            "profileId": "management",
            "profileName": "Для руководства",
            "profileIcon": "📊",
        }
    return {
        "profileId": "security",
        "profileName": "Для отдела ИБ",
        "profileIcon": "🛡️",
    }


def _entry_from_daily_md(path: Path) -> dict | None:
    m = _MD_DAILY_RE.match(path.name)
    if not m:
        return None
    audience = m.group("audience")
    try:
        dt = datetime.strptime(
            f"{m.group('date')} {m.group('time').replace('-', ':')}",
            "%Y-%m-%d %H:%M",
        )
    except ValueError:
        dt = datetime.now()

    meta = _audience_meta(audience)
    return {
        "id": f"file-{path.stem}",
        "status": "done",
        "type": "daily",
        "query": "Ежедневный дайджест",
        "model": "—",
        "profileId": meta["profileId"],
        "profileName": meta["profileName"],
        "profileIcon": meta["profileIcon"],
        "preview": path.read_text(encoding="utf-8"),
        "articlesCount": 0,
        "sources": [],
        "sourcesCount": 0,
        "topicsCount": 0,
        "format": "md",
        "createdAt": dt.isoformat(),
        "durationSec": 0,
        "md_path": str(path),
        "json_path": None,
    }


def _entry_from_monthly_md(path: Path) -> dict | None:
    m = _MD_MONTHLY_RE.match(path.name)
    if not m:
        return None
    audience = m.group("audience")
    meta = _audience_meta(audience)
    return {
        "id": f"file-{path.stem}",
        "status": "done",
        "type": "monthly",
        "query": "Месячная выжимка",
        "model": "—",
        "profileId": meta["profileId"],
        "profileName": meta["profileName"],
        "profileIcon": meta["profileIcon"],
        "preview": path.read_text(encoding="utf-8"),
        "articlesCount": 0,
        "sources": [],
        "sourcesCount": 0,
        "topicsCount": 0,
        "format": "md",
        "createdAt": datetime.now().isoformat(),
        "durationSec": 0,
        "md_path": str(path),
        "json_path": None,
    }


def load_digests_from_disk() -> None:
    """Читает только output/*.json. Файлы .md остаются на диске,
    но в истории не используются — чтобы не было дублей."""
    global DIGESTS
    output = Path("output")
    if not output.exists():
        return

    loaded = 0
    for meta_path in output.glob("*.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            digest_id = meta.get("id")
            if digest_id:
                DIGESTS[digest_id] = meta
                loaded += 1
        except Exception:
            continue

    print(f"[storage] загружено дайджестов из JSON: {loaded}")


def _read_yaml(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def _normalize_source_for_ui(src: dict) -> dict:
    """Дополняет источник полями, которые ждёт фронт."""
    out = dict(src)
    if "group" not in out:
        type_to_group = {"telegram": "telegram", "website": "official", "rss": "news"}
        out["group"] = type_to_group.get(out.get("type", "rss"), "news")
    out.setdefault("articlesPerDay", 0)
    out.setdefault("lastFetch", "ещё не загружался")
    out.setdefault("status", "ok")
    return out


def load_sources() -> list[dict]:
    data = _read_yaml("config/sources.yaml")
    raw = data.get("sources", [])
    return [_normalize_source_for_ui(s) for s in raw]


def save_sources() -> None:
    """Записывает SOURCES в config/sources.yaml. Вычисляемые поля отбрасываются."""
    path = Path("config/sources.yaml")
    clean = []
    for s in SOURCES:
        c = {k: v for k, v in s.items()
             if k not in ("articlesPerDay", "lastFetch", "status", "errorMessage")}
        clean.append(c)
    path.write_text(
        yaml.safe_dump({"sources": clean}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


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
    global SOURCES, PROFILES, SETTINGS
    SOURCES = load_sources()
    PROFILES = load_profiles()
    load_digests_from_disk()
    SETTINGS = load_settings()