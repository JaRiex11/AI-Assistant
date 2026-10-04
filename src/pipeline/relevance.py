# src/pipeline/relevance.py
import numpy as np
from src.models.publication import Publication
from src.utils.embedder import Embedder


class RelevanceFilter:
    def __init__(self, embedder: Embedder, k: float = 2.0, min_results: int = 5):
        self.embedder = embedder
        self.k = k                    # коэффициент для MAD: чем больше, тем строже отбор
        self.min_results = min_results  # минимум статей в дайджесте

    def _profile_to_text(self, profile: dict) -> str:
        """Собирает профиль интересов в один текст для эмбеддинга."""
        parts = [
            profile.get("name", ""),
            profile.get("description", ""),
            " ".join(profile.get("focus_topics", [])),
            " ".join(profile.get("angle", [])),
        ]
        return " ".join(parts)

    async def filter(self, pubs: list[Publication], profile: dict) -> list[Publication]:
        if not pubs:
            return []

        # 1. Эмбеддинг профиля
        profile_text = self._profile_to_text(profile)
        profile_vec = np.array(await self.embedder.embed_one(profile_text))

        # 2. Эмбеддинги публикаций
        texts = [f"{p.title}. {p.text or ''}"[:4000] for p in pubs]
        print(f"[relevance] считаем эмбеддинги для {len(texts)} публикаций...")
        pub_vecs = await self.embedder.embed_many(texts)

        # 3. Косинусная близость
        scores = Embedder.cosine_similarity(profile_vec, pub_vecs)

        # 4. Присваиваем скорам всем
        for pub, score in zip(pubs, scores):
            pub.relevance_score = float(score)

        # 5. ДИНАМИЧЕСКИЙ ПОРОГ: median + k * MAD
        median = float(np.median(scores))
        mad = float(np.median(np.abs(scores - median)))
        threshold = median + self.k * mad

        print(f"\n[relevance] режим: median + {self.k}·MAD")
        print(f"[relevance] медиана: {median:.3f}, MAD: {mad:.3f}")
        print(f"[relevance] порог: {threshold:.3f}")

        # 6. Фильтрация по порогу
        result = []
        for pub in pubs:
            if pub.relevance_score >= threshold:
                result.append(pub)
            else:
                pub.rejection_reason = f"below_threshold ({pub.relevance_score:.3f})"

        # 7. Fallback: если прошло меньше min_results, добираем топ-N
        if len(result) < self.min_results:
            print(f"[relevance] прошло {len(result)} < min {self.min_results}, добираем топ")
            # сортируем всех по скору
            all_sorted = sorted(pubs, key=lambda p: p.relevance_score, reverse=True)
            result = all_sorted[:self.min_results]
            for pub in result:
                pub.rejection_reason = None   # сбрасываем — теперь проходят

        # 8. Сортировка и диагностика
        result.sort(key=lambda p: p.relevance_score, reverse=True)
        print(f"[relevance] прошло: {len(result)}/{len(pubs)}")
        top5 = sorted(scores, reverse=True)[:5]
        print(f"[relevance] топ-5 скоров: {[f'{s:.3f}' for s in top5]}\n")

        return result