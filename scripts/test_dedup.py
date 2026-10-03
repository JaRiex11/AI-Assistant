import asyncio
from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer
from src.pipeline.deduplicator import Deduplicator


async def main():
    raw = await Collector().collect_all()
    pubs = Normalizer().normalize_all(raw)
    print(f"После нормализации: {len(pubs)}")

    # --- искусственные дубли для теста ---
    if pubs:
        import copy
        fake1 = copy.deepcopy(pubs[0])
        fake1.id = "fake_dup_1"
        fake1.title = pubs[0].title + " — подробности"   # похожий, но не идентичный

        fake2 = copy.deepcopy(pubs[1])
        fake2.id = "fake_dup_2"
        fake2.title = "ПОДРОБНОСТИ: " + pubs[1].title.lower()

        fake3 = copy.deepcopy(pubs[2])   # точная копия (но с другим id)
        fake3.id = "fake_dup_3"

        pubs.extend([fake1, fake2, fake3])
        print(f"Добавили 3 искусственных дубля → {len(pubs)}")

    # --- дедупликация ---
    deduped = Deduplicator(threshold=85).deduplicate(pubs)
    print(f"После дедупликации: {len(deduped)}")
    print(f"Отброшено: {len(pubs) - len(deduped)}")

    # --- что попало в отброшенные ---
    all_ids = {p.id for p in deduped}
    dropped = [p for p in pubs if p.id not in all_ids]
    if dropped:
        print("\n=== ОТБРОШЕНЫ ===")
        for p in dropped:
            print(f"  ↳ {p.title[:70]}")
            print(f"    причина: {p.rejection_reason}")


if __name__ == "__main__":
    asyncio.run(main())