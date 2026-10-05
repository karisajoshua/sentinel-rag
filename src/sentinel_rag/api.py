from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .domain import GroundedAnswer, SourceDocument

router = APIRouter(prefix="/api/v1")


class IndexRequest(BaseModel):
    repository: str = Field(min_length=3, pattern=r"^[^/\s]+/[^/\s]+$")
    documents: list[SourceDocument]


class IndexResponse(BaseModel):
    repository: str
    chunks_indexed: int


class QuestionRequest(BaseModel):
    repository: str = Field(min_length=3, pattern=r"^[^/\s]+/[^/\s]+$")
    question: str = Field(min_length=3, max_length=4000)
    limit: int = Field(default=5, ge=1, le=20)


class IndexService(Protocol):
    def index(self, documents: list[SourceDocument]) -> int: ...


class QAService(Protocol):
    def ask(self, repository: str, question: str, limit: int = 5) -> GroundedAnswer: ...


def unavailable_indexer() -> IndexService:
    raise HTTPException(status_code=503, detail="Indexer is not configured")


def unavailable_qa() -> QAService:
    raise HTTPException(status_code=503, detail="Grounded QA is not configured")


@router.post("/repositories/index", response_model=IndexResponse)
def index_repository(
    request: IndexRequest,
    indexer: IndexService = Depends(unavailable_indexer),
) -> IndexResponse:
    if any(document.repository != request.repository for document in request.documents):
        raise HTTPException(status_code=422, detail="Document repository does not match request")
    count = indexer.index(request.documents)
    return IndexResponse(repository=request.repository, chunks_indexed=count)


@router.post("/questions", response_model=GroundedAnswer)
def ask_question(
    request: QuestionRequest,
    qa: QAService = Depends(unavailable_qa),
) -> GroundedAnswer:
    return qa.ask(request.repository, request.question, request.limit)
