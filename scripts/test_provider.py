import asyncio
from src.providers.ollama import OllamaProvider

async def check(model_name):
    print(f"\n=== {model_name} ===")
    provider = OllamaProvider(model=model_name, config={"temperature": 0, "seed": 42})
    answer = await provider.complete("Ответь ровно одним словом: работает?")
    print("Ответ:", answer)

async def main():
    for model in ["qwen3:4b"]: #"deepseek-v4-pro:cloud", 
        await check(model)

if __name__ == "__main__":
    asyncio.run(main())