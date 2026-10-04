from datetime import datetime
from pathlib import Path

from src.models.publication import Publication
from src.pipeline.grouper import SECTION_ORDER, SECTION_TITLES
from datetime import datetime


class Exporter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def render_markdown(
        self,
        groups: dict[str, list[Publication]],
        total_collected: int,
        sources_count: int,
    ) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        total_in_digest = sum(len(v) for v in groups.values())

        lines = [
            f"# ИТ/ИБ дайджест — {date_str}",
            "",
            f"*Собрано: {total_collected} публикаций из {sources_count} источников. "
            f"В дайджест вошло: {total_in_digest}.*",
            "",
        ]

        for section_type in SECTION_ORDER:
            pubs = groups.get(section_type, [])
            if not pubs:
                continue

            lines.append(f"## {SECTION_TITLES[section_type]} ({len(pubs)})")
            lines.append("")

            for pub in pubs:
                lines.append(self._render_publication(pub))

            lines.append("")

        return "\n".join(lines)

    def _render_publication(self, pub: Publication) -> str:
        title = pub.title.strip().rstrip(".")
        annotation = self._make_annotation(pub)
        url = str(pub.url)
        source = pub.source_name

        return (
            f"- **{title}** — {annotation}  \n"
            f"  <sub>[{source}]({url})</sub>"
        )

    @staticmethod
    def _make_annotation(pub: Publication, max_len: int = 180) -> str:
        """Первые N символов текста. Без LLM — быстро и дёшево."""
        text = (pub.text or "").strip()
        if not text:
            return ""
        if len(text) <= max_len:
            return text
        # обрезаем по границе слова
        cut = text[:max_len].rsplit(" ", 1)[0]
        return cut + "…"

    def save(self, content: str, audience: str, keep_latest: bool = True) -> Path:
        """
        Сохраняет дайджест с временной меткой в имени.
        Опционально создаёт/перезаписывает файл digest_{audience}_latest.md
        как ярлык на последний дайджест.
        """

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"digest_{audience}_{timestamp}.md"

        path = self.output_dir / filename
        path.write_text(content, encoding="utf-8")

        # дублируем в latest — удобно для быстрой проверки
        if keep_latest:
            latest = self.output_dir / f"digest_{audience}_latest.md"
            latest.write_text(content, encoding="utf-8")

        return path