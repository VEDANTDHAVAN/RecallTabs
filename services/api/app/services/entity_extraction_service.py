import json

from app.services.llm_service import LLMService

class EntityExtractionService:
    def __init__(self):
        self.llm = LLMService()

    def extract(self, title: str, content: str) -> list[dict]:
        prompt = f"""
You are an expert knowledge graph extraction engine.

Extract every important entity from the webpage.

Include:
- People
- Companies
- Organizations
- Research Papers
- Libraries
- Frameworks
- Programming Languages
- Technologies
- Databases
- Products
- APIs
- Standards
- Concepts
- Tools

Ignore:
- Generic words
- Stop words
- Navigation text
- Menu Items

Return ONLY valid JSON.

Format: [
 {{
   "name":"FastAPI",
   "type":"Framework",
   "summary":"Modern Python web framework."
 }},
 {{
   "name":"OpenAI",
   "type":"Company",
   "summary":"AI research company."
 }}
]

Title: {title}
Content: {content[:12000]}
"""
        
        response = self.llm.chat(
            question=prompt, context="",
            history=[],
        )

        try:
            response_text = response or ""
            entities = json.loads(response_text)

            if isinstance(entities, list):
                return entities
        
        except Exception:
            pass 

        return []