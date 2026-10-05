from sentinel_rag.domain import Citation, GroundedAnswer, RetrievedChunk
from sentinel_rag.evaluation import EvaluationCase, aggregate, evaluate


def test_evaluation_measures_rank_and_citation_coverage() -> None:
    case = EvaluationCase("Which Python?", frozenset({".github/workflows/ci.yml"}))
    retrieved = [
        RetrievedChunk(path="README.md", content="docs", score=0.9),
        RetrievedChunk(path=".github/workflows/ci.yml", content="3.12", score=0.8),
    ]
    answer = GroundedAnswer(
        answer="Python 3.12",
        citations=[Citation(path=".github/workflows/ci.yml", start_line=1, end_line=1)],
        confidence=0.8,
        status="grounded",
    )
    result = evaluate(case, retrieved, answer)
    assert result.retrieval_hit
    assert result.reciprocal_rank == 0.5
    assert result.citation_coverage == 1.0
    assert aggregate([result])["retrieval_hit_rate"] == 1.0


def test_empty_evaluation_aggregate_is_explicit_zero() -> None:
    assert aggregate([])["grounded_rate"] == 0.0
