import ollama
import numpy as np


class Embedder:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
        self.client = ollama.AsyncClient()      # без host - локальный Ollama

    async def embed_one(self, text: str) -> list[float]:
        r = await self.client.embeddings(model=self.model, prompt=text)
        return r["embedding"]

    async def embed_many(self, texts: list[str]) -> np.ndarray:
        vectors = []
        for i, t in enumerate(texts):
            v = await self.embed_one(t[:4000])
            vectors.append(v)
            if (i + 1) % 20 == 0:
                print(f"[embedder] {i + 1}/{len(texts)}")
        return np.array(vectors)

    @staticmethod
    def cosine_similarity(profile_vec: np.ndarray, pub_vecs: np.ndarray) -> np.ndarray:
        a = profile_vec / np.linalg.norm(profile_vec)
        b = pub_vecs / np.linalg.norm(pub_vecs, axis=1, keepdims=True)
        return b @ a