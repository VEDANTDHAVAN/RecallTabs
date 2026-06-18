from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class LLMService:
    def answer(
      self, question: str, context: str,  
    ):
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[
                {
                    "role": "system",
                    "content": """You are RecallTabs, an AI memory assistant.
                    Use ONLY the provided context.
                    If the answer is unavailable: I couldn't find that information in your saved tabs.'
                    Always cite the sources mentally before answering.
                    Be concise."""
                },
                {
                    "role": "user",
                    "content": f"""Context: {context}, Question: {question}"""
                }
            ], temperature=0.2, max_tokens=300,
        )

        return response.choices[0].message.content