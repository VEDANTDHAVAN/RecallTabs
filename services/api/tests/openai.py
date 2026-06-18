from app.services.llm_service import LLMService

service = LLMService()

print(

    service.answer(

        "What is pgvector?",

        "pgvector is a PostgreSQL extension for vector similarity search."

    )

)