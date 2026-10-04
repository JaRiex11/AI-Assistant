# main.py
import argparse
import asyncio
from pathlib import Path

from src.utils.profile import ProfileLoader
from src.utils.categories import SourceCategories
from src.utils.prompts import PromptLoader
from src.utils.embedder import Embedder
from src.providers.ollama import OllamaProvider
from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.relevance import RelevanceFilter
from src.pipeline.classifier import Classifier
from src.pipeline.grouper import group_by_type
from src.pipeline.exporter import Exporter


async def run(audience: str):
    # 1. Профиль
    profile_loader = ProfileLoader("config/profile.yaml")
    profile = profile_loader.profile[audience] if audience in profile_loader.profile else profile_loader.profile
    # ВАЖНО: посмотрите свою структуру profile.yaml — возможно, там profiles[security|management]

    categories = SourceCategories("config/source_categories.yaml")

    # 2. Сбор
    raw = await Collector().collect_all(audience=audience)
    pubs = Normalizer().normalize_all(raw)
    pubs = Deduplicator(threshold=85).deduplicate(pubs)
    total_collected = len(pubs)
    print(f"Собрано: {total_collected}")

    # 3. Релевантность
    embedder = Embedder(model="bge-m3")
    relevance = RelevanceFilter(embedder, k=2.0, min_results=8)
    pubs = await relevance.filter(pubs, profile)

    # 4. Классификация
    llm = OllamaProvider(
        model="gpt-oss:120b-cloud",
        config={"temperature": 0, "seed": 42},
    )
    classifier = Classifier(llm, PromptLoader("prompts"), categories)
    pubs = await classifier.classify_all(pubs)

    # 5. Группировка + экспорт
    groups = group_by_type(pubs)
    exporter = Exporter()
    markdown = exporter.render_markdown(
        groups,
        total_collected=total_collected,
        sources_count=len(categories.tech if audience == "tech" else categories.exec),
    )
    path = exporter.save(markdown, audience=audience)
    exporter.update_index()
    print(f"✅ {path}")


def main():
    parser = argparse.ArgumentParser(description="Генератор ИТ/ИБ дайджестов")
    parser.add_argument(
        "--audience", "-a",
        choices=["tech", "exec"],
        default=None,
        help="Аудитория дайджеста. Если не задана — берётся из profile.yaml",
    )
    parser.add_argument(
        "--monthly", "-m",
        action="store_true",
        help="Собрать месячную выжимку из сохранённых дайджестов",
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=30,
        help="Период в днях (по умолчанию 30)",
    )
    args = parser.parse_args()

    if args.audience is None:
        audience = ProfileLoader("config/profile.yaml").audience
    else:
        audience = args.audience

    if args.monthly:
        from src.pipeline.monthly import MonthlyDigest

        llm = OllamaProvider(
            model="gpt-oss:120b-cloud",
            config={"temperature": 0, "seed": 42},
        )
        monthly = MonthlyDigest("output")
        path = asyncio.run(
            monthly.build(
                audience=audience,
                llm=llm,
                loader=PromptLoader("prompts"),
                days=args.days,
            )
        )
        if path:
            print(f"✅ Месячный дайджест: {path}")
        else:
            print("⚠️ Дайджестов за период не найдено")
        return

    # иначе — обычный daily-пайплайн
    asyncio.run(run(audience))


if __name__ == "__main__":
    main()