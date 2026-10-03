import feedparser
import httpx
import yaml
from pathlib import Path


class Collector:
    def __init__(self, sources_path: str = "config/sources.yaml"):
        self.sources_path = Path(sources_path)

    def _load_sources(self) -> list[dict]:
        data = yaml.safe_load(self.sources_path.read_text(encoding="utf-8"))
        return [s for s in data["sources"] if s.get("active", True)]

    async def _fetch_one(self, client: httpx.AsyncClient, source: dict) -> list[dict]:
        """Скачивает один RSS-фид, возвращает список сырых записей."""
        try:
            r = await client.get(
            source["url"],
            timeout=30,
            follow_redirects=True,     # ← идти по 301/302
        )
            r.raise_for_status()
        except Exception as e:
            print(f"[collector] {source['id']}: ошибка сети — {e}")
            return []

        feed = feedparser.parse(r.content)
        items = []
        for entry in feed.entries:
            items.append({
                "source_id": source["id"],
                "source_name": source["name"],
                "source_category": source.get("category", "tech"),
                "lang": source.get("lang", "ru"),
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", "").strip(),
                "summary": entry.get("summary", "").strip(),
                "published": entry.get("published", ""),
            })
        return items

    async def collect_all(self) -> list[dict]:
        """Собирает все активные источники асинхронно."""
        sources = self._load_sources()
        async with httpx.AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0 Safari/537.36",
                "Accept": "application/rss+xml, application/xml, text/xml, */*",
            }
        ) as client:
            import asyncio
            results = await asyncio.gather(
                *[self._fetch_one(client, s) for s in sources]
            )

        all_items = []
        for src, items in zip(sources, results):
            print(f"[collector] {src['id']}: {len(items)} записей")
            all_items.extend(items)
        return all_items