# src/providers/ollama.py
import os
import ollama
from .base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        model: str,
        config: dict | None = None,
        api_key: str | None = None,
        host: str | None = None,
        cloud: bool | None = None,
    ):
        self.model = model
        self.config = config or {}
        self.api_key = api_key or os.environ.get("OLLAMA_API_KEY")

        if host:
            self.host = host
        elif cloud is True:
            self.host = "https://ollama.com"
        elif cloud is False:
            self.host = "http://localhost:11434"
        elif self.api_key:
            self.host = "https://ollama.com"
        else:
            self.host = "http://localhost:11434"

        if self.host == "https://ollama.com" and not self.api_key:
            raise ValueError(
                "Облачный режим требует OLLAMA_API_KEY. "
                "Задайте ключ или переключитесь в локальный режим."
            )

        headers = {}
        if self.api_key and self.host == "https://ollama.com":
            headers["Authorization"] = f"Bearer {self.api_key}"

        self.client = ollama.AsyncClient(host=self.host, headers=headers)
        

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
            "think": False
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