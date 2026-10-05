from collections.abc import Sequence

import psycopg

from .domain import RetrievedChunk
from .store import EmbeddedChunk


class PgVectorStore:
    """PostgreSQL/pgvector implementation of the vector-store boundary."""

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    @staticmethod
    def _vector(values: Sequence[float]) -> str:
        return "[" + ",".join(str(float(value)) for value in values) + "]"

    def upsert(self, chunks: Sequence[EmbeddedChunk]) -> None:
        if not chunks:
            return
        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                for item in chunks:
                    chunk = item.chunk
                    cursor.execute(
                        """
                        INSERT INTO repository_chunks
                            (repository, path, commit_sha, start_line, end_line, content, embedding)
                        VALUES (%s, %s, %s, %s, %s, %s, %s::vector)
                        ON CONFLICT (repository, path, commit_sha, start_line, end_line)
                        DO UPDATE SET content = EXCLUDED.content, embedding = EXCLUDED.embedding
                        """,
                        (
                            chunk.repository, chunk.path, chunk.commit_sha,
                            chunk.start_line, chunk.end_line, chunk.content,
                            self._vector(item.embedding),
                        ),
                    )

    def search(
        self, repository: str, query_embedding: Sequence[float], limit: int = 5
    ) -> list[RetrievedChunk]:
        if limit < 1:
            return []
        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT path, content, 1 - (embedding <=> %s::vector) AS score,
                           start_line, end_line
                    FROM repository_chunks
                    WHERE repository = %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        self._vector(query_embedding), repository,
                        self._vector(query_embedding), limit,
                    ),
                )
                return [
                    RetrievedChunk(
                        path=row[0], content=row[1],
                        score=max(0.0, min(1.0, float(row[2]))),
                        start_line=row[3], end_line=row[4],
                    )
                    for row in cursor.fetchall()
                ]
