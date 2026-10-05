import pytest

from sentinel_rag.chunking import chunk_document
from sentinel_rag.domain import SourceDocument


def document(content: str) -> SourceDocument:
    return SourceDocument(repository="owner/repo", path="app.py", content=content, commit_sha="abc")


def test_chunking_preserves_line_evidence() -> None:
    chunks = chunk_document(document("\n".join(f"line {i}" for i in range(1, 7))), max_lines=4, overlap=1)
    assert [(c.start_line, c.end_line) for c in chunks] == [(1, 4), (4, 6)]
    assert chunks[1].content.startswith("line 4")


def test_chunking_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_document(document("content"), max_lines=5, overlap=5)
