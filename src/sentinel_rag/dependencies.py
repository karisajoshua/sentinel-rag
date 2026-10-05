from functools import lru_cache

from fastapi import HTTPException

from .config import get_settings
from .openai_embeddings import OpenAIEmbeddingProvider
from .pgvector_store import PgVectorStore
from .qa import GroundedQA
from .retrieval import RepositoryIndexer, SemanticRetriever
from .llm import OpenAILanguageModel


@lru_cache
def build_indexer() -> RepositoryIndexer:
    settings = get_settings()
    if not settings.database_url or not settings.openai_api_key:
        raise HTTPException(status_code=503, detail="AI infrastructure is not configured")
    embeddings = OpenAIEmbeddingProvider(settings.openai_api_key)
    return RepositoryIndexer(embeddings, PgVectorStore(settings.database_url))


@lru_cache
def build_qa() -> GroundedQA:
    settings = get_settings()
    if not settings.database_url or not settings.openai_api_key:
        raise HTTPException(status_code=503, detail="AI infrastructure is not configured")
    embeddings = OpenAIEmbeddingProvider(settings.openai_api_key)
    retriever = SemanticRetriever(embeddings, PgVectorStore(settings.database_url))
    model = OpenAILanguageModel(settings.openai_api_key, settings.openai_chat_model)
    return GroundedQA(retriever, model)
