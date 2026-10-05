from dataclasses import dataclass
from typing import Protocol

from .domain import SourceDocument

DEFAULT_EXTENSIONS = {
    ".md", ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".toml", ".yaml", ".yml"
}


@dataclass(frozen=True)
class RepositoryFile:
    path: str
    content: str
    commit_sha: str


class RepositorySource(Protocol):
    def files(self, repository: str) -> list[RepositoryFile]: ...


def ingest_repository(source: RepositorySource, repository: str) -> list[SourceDocument]:
    documents: list[SourceDocument] = []
    for item in source.files(repository):
        suffix = "." + item.path.rsplit(".", 1)[-1].lower() if "." in item.path else ""
        if suffix not in DEFAULT_EXTENSIONS:
            continue
        documents.append(
            SourceDocument(
                repository=repository,
                path=item.path,
                content=item.content,
                commit_sha=item.commit_sha,
            )
        )
    return documents
