import asyncio
import json
from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider


async def main():
    loader = PromptLoader("prompts")
    llm = OllamaProvider(
        model="qwen3:4b",
        config={"temperature": 0, "seed": 42, "max_tokens": 512},
    )

    prompt = loader.render(
        "classify_publication.jinja2",
        title="Атака PhantomCore на промышленный сектор РФ",
        text="Группировка атаковала предприятия через фишинг с KermitRAT.",
        source="https://www.f6.ru/blog/phantomcore-newtools/",
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
                "reason": {"type": "string"},
            },
            "required": ["type", "reason"],
        },
    )

    print(raw)
    parsed = json.loads(raw)
    print("=== РАСПАРСЕНО ===")
    print(parsed["type"], "|", parsed["reason"])


if __name__ == "__main__":
    asyncio.run(main())