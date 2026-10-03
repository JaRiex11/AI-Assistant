import asyncio
import json

# import src.utils.prompts as pr
# import src.providers.ollama as oll
from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider


async def main():
    loader = PromptLoader("prompts")
    llm = OllamaProvider(
        # model="qwen3:4b",
        model='gpt-oss:120b-cloud',
        config={"temperature": 0, "seed": 42}#, "max_tokens": 512},
    )

    prompt = loader.render(
        "classify_publication.jinja2",
        # "test_prompt.jinja2",
        title="Атака PhantomCore на промышленный сектор РФ",
        text="Группировка атаковала предприятия через фишинг с KermitRAT.",
        source="https://www.f6.ru/blog/phantomcore-newtools/",
        tech_sources=[
        "https://habr.com",
        "https://xakep.ru",
        "@true_secator",
    ],
    exec_sources=[
        "https://cisoclub.ru",
        "https://www.kommersant.ru",
    ],
    )

    print("=== ПРОМПТ ===")
    print(prompt)
    print("=== ОТВЕТ ===")

    raw = await llm.complete(
        prompt,
        schema={
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
        "required": [
            "type", "priority", "tags", "confidence",
            "audience", "impactScore", "alert_worthy",
        ],
    },
    )

    print("=== RAW OUTPUT ===")
    print(repr(raw))          # repr покажет даже невидимые символы
    print("=== LENGTH ===", len(raw))

    print(raw)
    parsed = json.loads(raw)
    print("=== РАСПАРСЕНО ===")
    print("type:", parsed["type"])
    print("priority:", parsed["priority"])
    print("tags:", parsed["tags"])
    print("confidence:", parsed["confidence"])
    print("audience:", parsed["audience"])
    print("impactScore:", parsed["impactScore"])
    print("alert_worthy:", parsed["alert_worthy"])


if __name__ == "__main__":
    asyncio.run(main())