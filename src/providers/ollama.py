# src/providers/ollama.py
import ollama
from .base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self, model: str, config: dict | None = None):
        self.model = model
        self.config = config or {}
        self.client = ollama.AsyncClient()

    async def complete(self, prompt: str, schema: dict | None = None) -> str:
        options = {
            "temperature": self.config.get("temperature", 0),
            "seed": self.config.get("seed", 42),
            "num_predict": self.config.get("max_tokens", 2048),
        }

        kwargs = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "options": options,
        }
        if schema is not None:
            kwargs["format"] = schema

        response = await self.client.chat(**kwargs)
        return response["message"]["content"]

    async def embed(self, texts: list[str], model: str = "bge-m3") -> list[list[float]]:
        result = []
        for t in texts:
            r = await self.client.embeddings(model=model, prompt=t)
            result.append(r["embedding"])
        return result