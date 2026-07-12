import json
from app.services.llm_service import LLMService

PROMPT = """
Extract relationships between entities.
Return ONLY JSON.

Format:
[
 {
   "source":"Transformer",
   "relation":"uses",
   "target":"Attention",
 }
]

Text: {text}
"""

class RelationshipExtractionService:
    def __init__(self):
        self.llm = LLMService()

    def extract(self, text: str):
        response = self.llm.complete(
            PROMPT.format(text=text)
        )

        try:
            return json.loads(response)
        except Exception:
            return []