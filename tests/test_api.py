from fastapi.testclient import TestClient

from sentinel_rag.api import unavailable_indexer, unavailable_qa
from sentinel_rag.domain import GroundedAnswer
from sentinel_rag.main import app


class FakeIndexer:
    def index(self, documents: list) -> int:
        return len(documents)


class FakeQA:
    def ask(self, repository: str, question: str, limit: int = 5) -> GroundedAnswer:
        return GroundedAnswer(
            answer="Evidence-backed response",
            citations=[],
            confidence=0.7,
            status="grounded",
        )


def test_index_endpoint_uses_injected_service() -> None:
    app.dependency_overrides[unavailable_indexer] = lambda: FakeIndexer()
    client = TestClient(app)
    response = client.post("/api/v1/repositories/index", json={
        "repository": "owner/repo",
        "documents": [{
            "repository": "owner/repo",
            "path": "README.md",
            "content": "hello",
            "commit_sha": "abc",
        }],
    })
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["chunks_indexed"] == 1


def test_question_endpoint_validates_question_length() -> None:
    app.dependency_overrides[unavailable_qa] = lambda: FakeQA()
    client = TestClient(app)
    response = client.post("/api/v1/questions", json={
        "repository": "owner/repo",
        "question": "x",
    })
    app.dependency_overrides.clear()
    assert response.status_code == 422
