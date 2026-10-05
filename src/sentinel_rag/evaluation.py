from dataclasses import dataclass
from statistics import mean

from .domain import GroundedAnswer, RetrievedChunk


@dataclass(frozen=True)
class EvaluationCase:
    question: str
    expected_paths: frozenset[str]


@dataclass(frozen=True)
class EvaluationResult:
    retrieval_hit: bool
    reciprocal_rank: float
    citation_coverage: float
    grounded: bool


def evaluate(
    case: EvaluationCase,
    retrieved: list[RetrievedChunk],
    answer: GroundedAnswer,
) -> EvaluationResult:
    ranked_paths = [chunk.path for chunk in retrieved]
    matching_ranks = [
        index for index, path in enumerate(ranked_paths, start=1) if path in case.expected_paths
    ]
    reciprocal_rank = 1.0 / min(matching_ranks) if matching_ranks else 0.0
    cited_paths = {citation.path for citation in answer.citations}
    citation_coverage = (
        len(cited_paths & case.expected_paths) / len(case.expected_paths)
        if case.expected_paths
        else 1.0
    )
    return EvaluationResult(
        retrieval_hit=bool(matching_ranks),
        reciprocal_rank=reciprocal_rank,
        citation_coverage=citation_coverage,
        grounded=answer.status == "grounded" and bool(answer.citations),
    )


def aggregate(results: list[EvaluationResult]) -> dict[str, float]:
    if not results:
        return {
            "retrieval_hit_rate": 0.0,
            "mean_reciprocal_rank": 0.0,
            "citation_coverage": 0.0,
            "grounded_rate": 0.0,
        }
    return {
        "retrieval_hit_rate": mean(float(item.retrieval_hit) for item in results),
        "mean_reciprocal_rank": mean(item.reciprocal_rank for item in results),
        "citation_coverage": mean(item.citation_coverage for item in results),
        "grounded_rate": mean(float(item.grounded) for item in results),
    }
