from dataclasses import dataclass
from typing import Protocol, Sequence

from .chunking import TextChunk
from .domain import RetrievedChunk


@dataclass(frozen=True)
class EmbeddedChunk:
    chunk: TextChunk
    embedding: Sequence[float]


class VectorStore(Protocol):
    def upsert(self, chunks: Sequence[EmbeddedChunk]) -> None: ...

    def search(
        self, repository: str, query_embedding: Sequence[float], limit: int = 5
    ) -> list[RetrievedChunk]: ...
