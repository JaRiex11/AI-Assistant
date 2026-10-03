import hashlib
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional

from src.models.publication import Publication


def _clean_html(text: str) -> str:
    """Убирает HTML-теги из summary."""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _make_id(url: str, title: str) -> str:
    """Стабильный id — по URL, если его нет, по заголовку."""
    key = url or title
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def _parse_date(raw: str) -> Optional[datetime]:
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw)
    except Exception:
        return None


class Normalizer:
    def normalize_all(self, items: list[dict]) -> list[Publication]:
        result: list[Publication] = []
        seen_ids: set[str] = set()

        for item in items:
            title = item.get("title", "").strip()
            link = item.get("link", "").strip()
            if not title or not link:
                continue

            pub_id = _make_id(link, title)
            if pub_id in seen_ids:
                continue
            seen_ids.add(pub_id)

            result.append(Publication(
                id=pub_id,
                title=title,
                text=_clean_html(item.get("summary", "")),
                url=link,
                source_id=item["source_id"],
                source_name=item["source_name"],
                published_at=_parse_date(item.get("published", "")),
                lang=item.get("lang", "ru"),
            ))

        return result