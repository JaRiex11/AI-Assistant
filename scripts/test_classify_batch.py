# scripts/test_classify_batch.py
import asyncio
from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer
from src.pipeline.deduplicator import Deduplicator     # ← добавили
from src.pipeline.classifier import Classifier
from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider


async def main():
    # --- Сбор и подготовка ---
    raw = await Collector().collect_all()
    pubs = Normalizer().normalize_all(raw)
    pubs = Deduplicator(threshold=85).deduplicate(pubs)    # ← дедупликация
    pubs = pubs[:15]                                       # ← ограничение для MVP

    print(f"\nКлассифицируем {len(pubs)} публикаций...\n")

    # --- Классификация ---
    llm = OllamaProvider(
        model="gpt-oss:120b-cloud",
        config={"temperature": 0, "seed": 42},
    )
    loader = PromptLoader("prompts")
    classifier = Classifier(llm, loader)

    result = await classifier.classify_all(pubs)

    # --- Вывод ---
    print("\n=== РЕЗУЛЬТАТ ===")
    for p in result:
        print(f"[{p.type}] impact={p.impact_score} | {p.title[:60]}")


if __name__ == "__main__":
    asyncio.run(main())