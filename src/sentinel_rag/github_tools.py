from typing import Any, Mapping, Protocol

from .tools import ToolDefinition, ToolError


class GitHubReader(Protocol):
    def read_file(self, repository: str, path: str, ref: str) -> str: ...
    def list_files(self, repository: str, ref: str) -> list[str]: ...


def _required_string(arguments: Mapping[str, Any], key: str) -> str:
    value = arguments.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ToolError(f"{key} must be a non-empty string")
    return value


def github_read_tools(reader: GitHubReader) -> list[ToolDefinition]:
    def read_file(arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        repository = _required_string(arguments, "repository")
        path = _required_string(arguments, "path")
        ref = _required_string(arguments, "ref")
        return {"path": path, "content": reader.read_file(repository, path, ref)}

    def list_files(arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        repository = _required_string(arguments, "repository")
        ref = _required_string(arguments, "ref")
        return {"files": reader.list_files(repository, ref)}

    return [
        ToolDefinition(
            name="github.read_file",
            description="Read one repository file at an explicit ref.",
            handler=read_file,
        ),
        ToolDefinition(
            name="github.list_files",
            description="List repository paths at an explicit ref.",
            handler=list_files,
        ),
    ]
