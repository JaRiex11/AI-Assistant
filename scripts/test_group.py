import asyncio
from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.classifier import Classifier
from src.pipeline.grouper import group_by_type, SECTION_TITLES
from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider


async def main():
    # Собираем пайплайн до группировки
    raw = await Collector().collect_all()
    pubs = Normalizer().normalize_all(raw)
    pubs = Deduplicator(threshold=85).deduplicate(pubs)
    pubs = pubs[:15]

    llm = OllamaProvider(
        model="gpt-oss:120b-cloud",
        config={"temperature": 0, "seed": 42},
    )
    classifier = Classifier(llm, PromptLoader("prompts"))
    pubs = await classifier.classify_all(pubs)

    # ←←← ГРУППИРОВКА
    groups = group_by_type(pubs)

    print("\n=== ГРУППЫ ===")
    for t in groups:
        count = len(groups[t])
        print(f"{SECTION_TITLES[t]}: {count}")
        for p in groups[t][:3]:     # показываем по 3 примера
            print(f"  · [{p.impact_score}] {p.title[:70]}")


if __name__ == "__main__":
    asyncio.run(main())