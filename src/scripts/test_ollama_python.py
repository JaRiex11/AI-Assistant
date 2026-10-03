import ollama

response = ollama.chat(
    model="qwen3:4b",
    messages=[{"role": "user", "content": "Ответь одним словом: работает?"}],
)
print(response["message"]["content"])