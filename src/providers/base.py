# src/providers/base.py
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, schema: dict | None = None) -> dict | str: ...
    
    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]: ...