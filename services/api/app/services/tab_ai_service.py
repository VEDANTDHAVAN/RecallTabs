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

        if response is None:
            raise ValueError("LLM returned empty response.")

        analysis = json.loads(response)

        print(analysis)

        return analysis