from openai import OpenAI
from app.core.config import get_settings

from typing import Generator

from openai.types.chat import (
    ChatCompletionMessageParam, 
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
)

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
                    "content": """
You are RecallTabs, an AI memory assistant.

You answer ONLY from the provided browsing context.

If the answer is not present in the context, reply exactly:

I couldn't find that information in your saved tabs.

Be concise and factual.
"""
                },
                {
                    "role": "user",
                    "content": f"""
                Use the following saved browser context to answer.
                CONTEXT: {context}
                QUESTION: {question}

Answer only using the context above.
If the answer cannot be found in the context, say:
"I couldn't find that information in your saved tabs."
"""
                }
            ], temperature=0.2, max_tokens=300,
        )
        print(context)

        return response.choices[0].message.content or ""
    
    def complete(self, prompt: str):
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{
                "role": "system", "content": "Return valid JSON only."
            },{
                "role": "user", "content": prompt
            }],
        temperature=0
        )

        return response.choices[0].message.content or ""
    
    def chat(self, question: str, context: str, history: list):
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": """You are RecallTabs.
You answer questions using the user's saved browser memory.

Use:
1. Retrieved memory context
2. Previous conversation history

If information is unavailable, say:
'I couldn't find that information in your saved tabs.'

Be concise and accurate."""
            }
        ]
        messages.extend(history)

        messages.append({
            "role": "user",
            "content": f"""
Context: {context} Question: {question}
"""
        })

        response = client.chat.completions.create(
            model="gpt-4.1-mini", messages=messages,
            temperature=0.2, max_tokens=500,
        )

        return response.choices[0].message.content or ""
    
    def stream_chat(
        self, question: str, context: str,
        history: list[dict],
    ) -> Generator[str, None, None]:
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(
                role="system", content=(
                    "You answer questions using ONLY the provided context."
                    "If the answwr cannot be found , say you don't know."
                ),
            ),
            ChatCompletionSystemMessageParam(
                role="system", content=f"Context:\n{context}",
            ),
        ]

        # Add previous conversations
        for message in history:
            if message["role"] == "user":
                messages.append(
                    ChatCompletionUserMessageParam(
                        role="user", content=message["content"],
                    )
                )
            else:
                messages.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant", content=message["content"],
                    )
                )
        
        # Current question
        messages.append(
            ChatCompletionUserMessageParam(
                role="user", content=question,
            )
        )

        response = client.chat.completions.create(
            model="gpt-5", messages=messages,
            temperature=0.2, stream=True,
        )

        for chunk in response:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                yield delta.content

    def json_chat(self, prompt: str):
        return self.chat(question=prompt,
          context="", history=[],
        )