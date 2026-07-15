import json

from app.services.llm_service import LLMService

class TabAIService:
    def __init__(self):
        self.llm = LLMService()

    def analyze(self, content: str):
        prompt = f"""
Analyze this webpage. Return ONLY JSON.
Format:{{
"summary":"",
"keywords":[],
"topic":"",
"category":""
}}

Rules:

- topic should be SHORT.
- Maximum 2-5 words.

Examples:

Bad:
"Agentic Reinforcement Learning in Large Language Models"

Good:
"Agentic AI"

Bad:
"Transformer in deep learning"

Good:
"Transformers"

Bad:
"Database Management and SQL Editing"

Good:
"Database Management"

Return JSON only.

Content:

{content}
"""
        
        response = self.llm.complete(prompt)

        if not response or not response.strip():
            raise ValueError("LLM returned empty response.")
        
        try:
            analysis = json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON returned by LLM:\n{response}"
            ) from e

        return analysis