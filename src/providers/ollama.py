import ollama

class OllamaProvider:
    def __init__(self, model: str, config: dict | None = None):
        self.model = model
        self.config = config or {}

    async def complete(self, prompt: str) -> str:
        client = ollama.AsyncClient()
        response = await client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": self.config.get("temperature", 0),
                "seed": self.config.get("seed", 42),
            },
        )
        return response["message"]["content"]