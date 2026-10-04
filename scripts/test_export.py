# scripts/test_export.py
import asyncio

from src.utils.profile import ProfileLoader
from src.utils.categories import SourceCategories
from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.classifier import Classifier
from src.pipeline.grouper import group_by_type
from src.pipeline.exporter import Exporter
from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider
from src.utils.embedder import Embedder
from src.pipeline.relevance import RelevanceFilter


async def main():
    # 1. Загружаем профиль — определяем активную аудиторию
    profile_loader = ProfileLoader("config/profile.yaml")
    audience = profile_loader.audience
    profile = profile_loader.profile
    print(f"Активный профиль: {profile_loader.active} → аудитория: {audience}")

    # 2. Загружаем категории источников (для промпта классификатора)
    categories = SourceCategories("config/source_categories.yaml")

    # 3. Собираем ТОЛЬКО источники активной категории
    raw = await Collector().collect_all(audience=audience)
    pubs = Normalizer().normalize_all(raw)
    pubs = Deduplicator(threshold=85).deduplicate(pubs)
    total_collected = len(pubs)

    # релевантность на ВСЕХ публикациях
    embedder = Embedder(model="bge-m3")
    relevance = RelevanceFilter(embedder, k=2.0, min_results=10)
    pubs = await relevance.filter(pubs, profile)

    pubs = pubs[:15]
    print(f"Классифицируем {len(pubs)} публикаций...\n")

    # 4. Классифицируем
    llm = OllamaProvider(
        model="gpt-oss:120b-cloud",
        config={"temperature": 0, "seed": 42},
    )
    classifier = Classifier(llm, PromptLoader("prompts"), categories)
    pubs = await classifier.classify_all(pubs)

    # 5. Группируем и сохраняем
    groups = group_by_type(pubs)
    exporter = Exporter()
    markdown = exporter.render_markdown(
        groups,
        total_collected=total_collected,
        sources_count=len(categories.tech) if audience == "tech" else len(categories.exec),
    )
    path = exporter.save(markdown, audience=audience)
    print(f"\n✅ Дайджест ({audience}) сохранён: {path}")


if __name__ == "__main__":
    asyncio.run(main())