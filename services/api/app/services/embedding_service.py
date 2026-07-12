from openai import OpenAI

from app.core.config import get_settings


class EmbeddingService:
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

        self.model = "text-embedding-3-small"

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=384,
        )

        return response.data[0].embedding

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=384,
        )

        return [
            item.embedding
            for item in response.data
        ]