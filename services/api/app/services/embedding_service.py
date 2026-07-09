from openai import OpenAI

from app.core.config import Settings


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(
            api_key=Settings.OPENAI_API_KEY,
        )

        self.model = "text-embedding-3-small"

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [
            item.embedding
            for item in response.data
        ]