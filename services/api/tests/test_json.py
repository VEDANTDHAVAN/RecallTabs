from ollama import Client
import json

client = Client(host="http://localhost:11434")

prompt = """
Return ONLY valid JSON.

{
  "topic": "",
  "summary": "",
  "keywords": []
}

Text:
Python is a programming language used for AI and web development.
"""

response = client.chat(
    model="phi3:mini",
    messages=[
        {
            "role": "system",
            "content": "Return only valid JSON."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])