CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS repository_chunks (
    id BIGSERIAL PRIMARY KEY,
    repository TEXT NOT NULL,
    path TEXT NOT NULL,
    commit_sha TEXT NOT NULL,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    UNIQUE (repository, path, commit_sha, start_line, end_line)
);

CREATE INDEX IF NOT EXISTS repository_chunks_embedding_idx
ON repository_chunks USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS repository_chunks_repository_idx
ON repository_chunks (repository);
