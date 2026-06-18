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

CONTENT:

{content[:4000]}
"""
        
        response = self.llm.complete(prompt)

        if response is None:
            raise ValueError("LLM returned empty response.")

        analysis = json.loads(response)

        print(analysis)

        return analysis