from dataclasses import dataclass

from .chunking import chunk_document
from .domain import RetrievedChunk, SourceDocument
from .embeddings import EmbeddingProvider
from .store import EmbeddedChunk, VectorStore


@dataclass
class RepositoryIndexer:
    embeddings: EmbeddingProvider
    store: VectorStore

    def index(self, documents: list[SourceDocument]) -> int:
        chunks = [chunk for document in documents for chunk in chunk_document(document)]
        vectors = self.embeddings.embed([chunk.content for chunk in chunks])
        self.store.upsert(
            [EmbeddedChunk(chunk=chunk, embedding=vector) for chunk, vector in zip(chunks, vectors)]
        )
        return len(chunks)


@dataclass
class SemanticRetriever:
    embeddings: EmbeddingProvider
    store: VectorStore

    def retrieve(self, repository: str, question: str, limit: int = 5) -> list[RetrievedChunk]:
        query_vector = self.embeddings.embed([question])[0]
        return self.store.search(repository, query_vector, limit)
