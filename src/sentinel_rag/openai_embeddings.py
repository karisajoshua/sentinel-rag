from collections.abc import Sequence

from openai import OpenAI


class OpenAIEmbeddingProvider:
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
    ) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(
            model=self.model,
            input=list(texts),
            dimensions=self.dimensions,
        )
        return [item.embedding for item in response.data]
