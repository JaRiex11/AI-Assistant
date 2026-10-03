from rapidfuzz import fuzz
from src.models.publication import Publication


class Deduplicator:
    def __init__(self, threshold: int = 85):
        """
        threshold — минимальная схожесть заголовков (0..100),
        при которой считаем публикации дублями.
        85 — безопасный дефолт для новостных заголовков.
        """
        self.threshold = threshold

    def deduplicate(self, pubs: list[Publication]) -> list[Publication]:
        result: list[Publication] = []
        seen_titles: list[tuple[str, str]] = []  # [(нормализованный_заголовок, id_оригинала)]

        for pub in pubs:
            norm_title = self._normalize_title(pub.title)
            duplicate_of = None

            for seen_title, seen_id in seen_titles:
                score = fuzz.token_set_ratio(norm_title, seen_title)
                if score >= self.threshold:
                    duplicate_of = seen_id
                    break

            if duplicate_of:
                pub.is_duplicate_of = duplicate_of
                pub.rejection_reason = f"near_duplicate (score >= {self.threshold})"
                # не добавляем в result — отбрасываем
                continue

            seen_titles.append((norm_title, pub.id))
            result.append(pub)

        return result

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Приводит заголовок к нижнему регистру, убирает пунктуацию и лишние пробелы."""
        import re
        title = title.lower()
        title = re.sub(r"[^\w\s]", " ", title, flags=re.UNICODE)
        title = re.sub(r"\s+", " ", title).strip()
        return title