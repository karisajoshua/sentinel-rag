from sentinel_rag.domain import RetrievedChunk
from sentinel_rag.qa import GroundedQA


class FakeRetriever:
    def __init__(self, results: list[RetrievedChunk]) -> None:
        self.results = results

    def retrieve(self, repository: str, question: str, limit: int = 5) -> list[RetrievedChunk]:
        return self.results[:limit]


class FakeModel:
    def __init__(self) -> None:
        self.called = False

    def answer(self, question: str, evidence: list[RetrievedChunk]) -> str:
        self.called = True
        return "CI uses Python 3.12."


def test_grounded_answer_contains_source_citation() -> None:
    model = FakeModel()
    qa = GroundedQA(
        FakeRetriever([
            RetrievedChunk(path=".github/workflows/ci.yml", content='python-version: "3.12"', score=0.91, start_line=12, end_line=12)
        ]),
        model,
    )
    result = qa.ask("owner/repo", "Which Python version does CI use?")
    assert result.status == "grounded"
    assert result.citations[0].path == ".github/workflows/ci.yml"
    assert result.confidence == 0.91
    assert model.called


def test_llm_is_not_called_without_sufficient_evidence() -> None:
    model = FakeModel()
    qa = GroundedQA(FakeRetriever([]), model)
    result = qa.ask("owner/repo", "Unknown?")
    assert result.status == "insufficient-evidence"
    assert result.citations == []
    assert not model.called
