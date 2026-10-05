import pytest

from sentinel_rag.github_tools import github_read_tools
from sentinel_rag.tools import ToolError, ToolInvocation, ToolRegistry


class Reader:
    def read_file(self, repository: str, path: str, ref: str) -> str:
        return "trusted only as data"

    def list_files(self, repository: str, ref: str) -> list[str]:
        return ["README.md", "src/app.py"]


def test_github_tool_requires_explicit_ref() -> None:
    registry = ToolRegistry(github_read_tools(Reader()))
    with pytest.raises(ToolError, match="ref"):
        registry.invoke(ToolInvocation("github.read_file", {
            "repository": "owner/repo",
            "path": "README.md",
        }))
