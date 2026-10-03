# src/providers/ollama.py
import ollama

class OllamaProvider(LLMProvider):
    def __init__(self, model: str, config: dict):
        self.model = model
        self.config = config  # temperature, seed, timeout
    
    async def complete(self, prompt, schema=None):
        response = await ollama.AsyncClient().chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            format=schema,  # JSON schema если нужно
            options={
                "temperature": self.config.get("temperature", 0),
                "seed": self.config.get("seed", 42),
            }
        )
        return response["message"]["content"]
    
    async def embed(self, texts):
        client = ollama.AsyncClient()
        return [ (await client.embeddings(model="bge-m3", prompt=t))["embedding"] 
                 for t in texts ]