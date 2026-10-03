import asyncio
from pathlib import Path
import yaml

from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.classifier import Classifier
from src.pipeline.grouper import group_by_type
from src.pipeline.exporter import Exporter
from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider


async def main():
    # --- Сбор ---
    raw = await Collector().collect_all()
    pubs = Normalizer().normalize_all(raw)
    pubs = Deduplicator(threshold=85).deduplicate(pubs)
    total_collected = len(pubs)
    pubs = pubs[:15]

    # --- Классификация ---
    llm = OllamaProvider(
        model="gpt-oss:120b-cloud",
        config={"temperature": 0, "seed": 42},
    )
    classifier = Classifier(llm, PromptLoader("prompts"))
    pubs = await classifier.classify_all(pubs)

    # --- Группировка ---
    groups = group_by_type(pubs)

    # --- Экспорт ---
    exporter = Exporter()
    markdown = exporter.render_markdown(
        groups,
        total_collected=total_collected,
        sources_count=1,               # временно, потом посчитаете из sources.yaml
    )
    path = exporter.save(markdown)

    print(f"\n✅ Дайджест сохранён: {path}")
    print(f"Размер: {len(markdown)} символов")


if __name__ == "__main__":
    asyncio.run(main())