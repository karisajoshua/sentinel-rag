# SentinelRAG

**Evidence-grounded AI repository intelligence.**

SentinelRAG is a production-oriented AI engineering project that will reason over real software repositories using retrieval-augmented generation, controlled tool calling, measurable evaluation, and explicit security boundaries.

## Architecture

```text
Repository
   |
   v
Ingestion -> Chunking -> Embeddings -> Vector Store
                                      |
Question -> Retrieval ----------------+
   |
   v
LLM reasoning -> Controlled tools -> Evidence-backed answer
   |
   +-> Evaluation
   +-> Tracing / latency / token and cost metrics
```

## Phase 1 — Foundation

Implemented now:

- Python 3.12+ package structure
- FastAPI service and health endpoint
- typed environment configuration
- typed RAG contracts for source documents, retrieved chunks, citations, and grounded answers
- pytest validation
- Ruff static checks
- GitHub Actions CI
- Docker deployment baseline
- initial AI security and trust boundaries

No LLM provider is wired in yet. Retrieval, generation, tool execution, and evaluation will be introduced behind explicit interfaces rather than coupled directly to the API.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn sentinel_rag.main:app --reload
```

Open `/docs` for the generated OpenAPI interface.

## Quality checks

```bash
ruff check .
pytest
```

## Roadmap

1. Repository ingestion and chunking
2. PostgreSQL + pgvector vector storage
3. Embeddings and semantic retrieval
4. LLM-grounded question answering
5. GitHub tool calling with least privilege
6. RAG and agent evaluation suite
7. OpenTelemetry observability
8. production deployment and evaluation dashboard

## License

Apache-2.0.
