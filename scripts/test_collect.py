import asyncio
from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer


async def main():
    collector = Collector()
    normalizer = Normalizer()

    print("=== СБОР ===")
    raw = await collector.collect_all()
    print(f"Сырых записей: {len(raw)}")

    # TODO: ЗДЕСЬ позже встроится фильтр релевантности:
    # raw = await relevance_filter.filter(raw, profile)

    print("\n=== НОРМАЛИЗАЦИЯ ===")
    pubs = normalizer.normalize_all(raw)
    print(f"Уникальных публикаций: {len(pubs)}")

    print("\n=== ПЕРВЫЕ 5 ===")
    for p in pubs[:5]:
        date = p.published_at.strftime("%Y-%m-%d") if p.published_at else "—"
        print(f"[{p.source_id}] {date} | {p.title[:80]}")


if __name__ == "__main__":
    asyncio.run(main())