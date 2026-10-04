# src/pipeline/classifier.py
import json
import re
from src.models.publication import Publication
from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider
from src.utils.categories import SourceCategories


def extract_json(text: str) -> str:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        return fence.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        return text[start:end + 1]
    return text


class Classifier:
    def __init__(
        self,
        llm: OllamaProvider,
        loader: PromptLoader,
        categories: SourceCategories
    ):
        self.llm = llm
        self.loader = loader
        self.categories = categories

    async def classify_one(self, pub: Publication) -> Publication:
        prompt = self.loader.render(
            "classify_publication.jinja2",
            title=pub.title,
            text=pub.text or pub.title,
            source=pub.url,
            tech_sources=self.categories.tech,       # ← из конфига
            exec_sources=self.categories.exec,       # ← из конфига
        )

        schema = {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["Атака", "Уязвимость", "Инфо"]},
                "priority": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "integer"}},
                "confidence": {"type": "number"},
                "audience": {"type": "string", "enum": ["tech", "exec", "unknown"]},
                "impactScore": {"type": "number"},
                "alert_worthy": {"type": "boolean"},
            },
            "required": ["type", "priority", "tags", "confidence",
                         "audience", "impactScore", "alert_worthy"],
        }

        try:
            raw = await self.llm.complete(prompt, schema=schema)
            data = json.loads(extract_json(raw))
        except Exception as e:
            print(f"[classifier] ошибка на '{pub.title[:50]}': {e}")
            pub.rejection_reason = f"llm_error: {e}"
            return pub

        pub.type = data.get("type")
        pub.priority = data.get("priority")
        pub.tags = data.get("tags", [])
        pub.confidence = data.get("confidence")
        pub.audience = data.get("audience")
        pub.impact_score = data.get("impactScore")
        pub.alert_worthy = data.get("alert_worthy")
        return pub

    async def classify_all(self, pubs: list[Publication]) -> list[Publication]:
        result = []
        for i, pub in enumerate(pubs, 1):
            print(f"[classifier] {i}/{len(pubs)}: {pub.title[:60]}")
            result.append(await self.classify_one(pub))
        return result