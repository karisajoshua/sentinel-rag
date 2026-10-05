from sentinel_rag.domain import RetrievedChunk, SourceDocument
from sentinel_rag.embeddings import DeterministicEmbeddingProvider
from sentinel_rag.retrieval import RepositoryIndexer, SemanticRetriever
from sentinel_rag.store import EmbeddedChunk


class MemoryStore:
    def __init__(self) -> None:
        self.items: list[EmbeddedChunk] = []

    def upsert(self, chunks: list[EmbeddedChunk]) -> None:
        self.items.extend(chunks)

    def search(self, repository: str, query_embedding: list[float], limit: int = 5) -> list[RetrievedChunk]:
        matching = [item for item in self.items if item.chunk.repository == repository]
        return [
            RetrievedChunk(
                path=item.chunk.path,
                content=item.chunk.content,
                score=1.0,
                start_line=item.chunk.start_line,
                end_line=item.chunk.end_line,
            )
            for item in matching[:limit]
        ]


def test_index_and_retrieve_are_provider_independent() -> None:
    store = MemoryStore()
    embeddings = DeterministicEmbeddingProvider()
    indexer = RepositoryIndexer(embeddings, store)
    count = indexer.index([
        SourceDocument(repository="owner/repo", path="README.md", content="security policy", commit_sha="abc")
    ])
    results = SemanticRetriever(embeddings, store).retrieve("owner/repo", "security")
    assert count == 1
    assert results[0].path == "README.md"
