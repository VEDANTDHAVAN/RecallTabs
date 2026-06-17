from fastembed import TextEmbedding

class EmbeddingService:
    def __init__(self):
        self.model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

    def embed(self, text: str) -> list[float]:
        embedding = list(
            self.model.embed([text])
        )[0]

        return embedding.tolist()