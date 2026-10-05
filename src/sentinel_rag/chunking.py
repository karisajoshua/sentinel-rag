from dataclasses import dataclass

from .domain import SourceDocument


@dataclass(frozen=True)
class TextChunk:
    repository: str
    path: str
    commit_sha: str
    content: str
    start_line: int
    end_line: int


def chunk_document(document: SourceDocument, max_lines: int = 80, overlap: int = 10) -> list[TextChunk]:
    if max_lines < 1:
        raise ValueError("max_lines must be positive")
    if overlap < 0 or overlap >= max_lines:
        raise ValueError("overlap must be >= 0 and less than max_lines")

    lines = document.content.splitlines()
    if not lines:
        return []

    chunks: list[TextChunk] = []
    step = max_lines - overlap
    for start in range(0, len(lines), step):
        selected = lines[start : start + max_lines]
        if not selected:
            break
        chunks.append(
            TextChunk(
                repository=document.repository,
                path=document.path,
                commit_sha=document.commit_sha,
                content="\n".join(selected),
                start_line=start + 1,
                end_line=start + len(selected),
            )
        )
        if start + max_lines >= len(lines):
            break
    return chunks
