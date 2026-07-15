from ollama import Client

client = Client(host="http://localhost:11434")

stream = client.chat(
    model="phi3:mini",
    stream=True,
    messages=[
        {
            "role": "user",
            "content": "Explain GraphRAG in 3 sentences."
        }
    ]
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)