import asyncio
from src.utils.embedder import Embedder


async def main():
    emb = Embedder()
    v = await emb.embed_one("Кибератака на промышленное предприятие РФ")
    print(f"Размер вектора: {len(v)}")
    print(f"Первые 5 значений: {v[:5]}")


if __name__ == "__main__":
    asyncio.run(main())