from app.services.tab_ai_service import TabAIService

service = TabAIService()

text = """
FastAPI is a Python framework.

It supports async programming.

It is commonly used for AI APIs.
"""

print(service.analyze(text))