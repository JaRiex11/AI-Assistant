# src/pipeline/orchestrator.py
from dataclasses import dataclass, field
from typing import Callable, Optional

from src.utils.profile import ProfileLoader
from src.utils.categories import SourceCategories
from src.utils.prompts import PromptLoader
from src.utils.embedder import Embedder
from src.utils.logger import log_event

from src.providers.ollama import OllamaProvider

from src.pipeline.collector import Collector
from src.pipeline.normalizer import Normalizer
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.relevance import RelevanceFilter
from src.pipeline.classifier import Classifier
from src.pipeline.grouper import group_by_type
from src.pipeline.exporter import Exporter


STAGES = ["collecting", "dedup", "relevance", "classify", "export"]


@dataclass
class PipelineStats:
    collected: int = 0
    after_dedup: int = 0
    after_relevance: int = 0
    after_classify: int = 0
    final: int = 0
    sources_count: int = 0
    stages_done: list[str] = field(default_factory=list)


async def run_full_pipeline(
    audience: str,
    progress_callback: Optional[Callable[[str], None]] = None,
    llm_model: str = "gpt-oss:120b-cloud",
    cloud: bool = True,
) -> tuple[str, PipelineStats]:
    """
    Полный пайплайн: RSS → Markdown.
    Возвращает (markdown, stats).
    """
    def notify(stage: str) -> None:
        if progress_callback:
            try:
                progress_callback(stage)
            except Exception:
                pass

    log_event({"stage": "pipeline", "action": "started", "audience": audience})
    stats = PipelineStats()

    # --- 1. Профиль ---
    loader = ProfileLoader("config/profile.yaml")
    profile = loader.get_by_audience(audience)
    categories = SourceCategories("config/source_categories.yaml")

    # --- 2. Сбор и нормализация ---
    notify("collecting")
    raw = await Collector().collect_all(audience=audience)
    pubs = Normalizer().normalize_all(raw)
    stats.collected = len(pubs)
    log_event({"stage": "pipeline", "action": "collected",
               "audience": audience, "count": stats.collected})

    # --- 3. Дедупликация ---
    notify("dedup")
    pubs = Deduplicator(threshold=85).deduplicate(pubs)
    stats.after_dedup = len(pubs)
    log_event({"stage": "pipeline", "action": "deduped",
               "count": stats.after_dedup})

    # --- 4. Фильтр релевантности ---
    notify("relevance")
    embedder = Embedder(model="bge-m3")
    relevance = RelevanceFilter(embedder, k=2.0, min_results=8)
    pubs = await relevance.filter(pubs, profile)
    stats.after_relevance = len(pubs)
    log_event({"stage": "pipeline", "action": "filtered",
               "count": stats.after_relevance})

    # --- 5. Классификация ---
    notify("classify")
    llm = OllamaProvider(
        model=llm_model,
        config={"temperature": 0, "seed": 42},
        cloud=cloud,
    )
    classifier = Classifier(llm, PromptLoader("prompts"), categories)
    pubs = await classifier.classify_all(pubs)
    stats.after_classify = len(pubs)
    log_event({"stage": "pipeline", "action": "classified",
               "count": stats.after_classify})

    # --- 6. Группировка + рендер Markdown ---
    notify("export")
    groups = group_by_type(pubs)
    stats.final = sum(len(v) for v in groups.values())
    stats.sources_count = len(
        categories.tech if audience == "tech" else categories.exec
    )

    exporter = Exporter()
    markdown = exporter.render_markdown(
        groups,
        total_collected=stats.collected,
        sources_count=stats.sources_count,
    )

    stats.stages_done = list(STAGES)
    log_event({"stage": "pipeline", "action": "finished",
               "audience": audience, "final": stats.final})

    return markdown, stats