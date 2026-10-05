from typing import Literal

from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    repository: str
    path: str
    content: str
    commit_sha: str


class RetrievedChunk(BaseModel):
    path: str
    content: str
    score: float = Field(ge=0.0, le=1.0)
    start_line: int | None = Field(default=None, ge=1)
    end_line: int | None = Field(default=None, ge=1)


class Citation(BaseModel):
    path: str
    start_line: int | None = None
    end_line: int | None = None


class GroundedAnswer(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float = Field(ge=0.0, le=1.0)
    status: Literal["grounded", "insufficient-evidence"]
