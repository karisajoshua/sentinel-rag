from sentinel_rag.github_ingestion import RepositoryFile, ingest_repository


class FakeSource:
    def files(self, repository: str) -> list[RepositoryFile]:
        return [
            RepositoryFile("src/app.py", "print('safe')", "sha1"),
            RepositoryFile("image.png", "binary-placeholder", "sha1"),
        ]


def test_ingestion_filters_unsupported_file_types() -> None:
    documents = ingest_repository(FakeSource(), "owner/repo")
    assert [document.path for document in documents] == ["src/app.py"]
    assert documents[0].repository == "owner/repo"
