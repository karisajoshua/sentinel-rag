import pytest
from pydantic import ValidationError

from sentinel_rag.domain import GroundedAnswer, RetrievedChunk


def test_retrieved_chunk_rejects_invalid_similarity_score() -> None:
    with pytest.raises(ValidationError):
        RetrievedChunk(path="README.md", content="evidence", score=1.1)


def test_grounded_answer_requires_bounded_confidence() -> None:
    with pytest.raises(ValidationError):
        GroundedAnswer(
            answer="Unsupported",
            citations=[],
            confidence=-0.1,
            status="insufficient-evidence",
        )
