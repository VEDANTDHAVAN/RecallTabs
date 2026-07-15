from app.services.llm_service import LLMService

llm = LLMService()

print(llm.complete(
    """Return valid JSON only.
    
    {
      "topic":"",
      "summary":"",
      "keywords":[]
    }

    Text: FastAPI is a modern Python framework.
    """
))