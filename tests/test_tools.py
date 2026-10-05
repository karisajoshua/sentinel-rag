import pytest

from sentinel_rag.tools import ToolDefinition, ToolError, ToolInvocation, ToolRegistry


def test_registry_rejects_mutating_tools() -> None:
    with pytest.raises(ToolError):
        ToolRegistry([
            ToolDefinition("github.write_file", "mutate", lambda args: {}, read_only=False)
        ])


def test_registry_rejects_non_allowlisted_invocation() -> None:
    registry = ToolRegistry([])
    with pytest.raises(ToolError):
        registry.invoke(ToolInvocation("shell.exec", {"command": "rm -rf /"}))
