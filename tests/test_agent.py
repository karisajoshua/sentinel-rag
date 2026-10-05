import pytest

from sentinel_rag.agent import ControlledAgent
from sentinel_rag.audit import MemoryAuditSink
from sentinel_rag.tools import ToolDefinition, ToolInvocation, ToolRegistry


class Planner:
    def __init__(self, calls: list[ToolInvocation]) -> None:
        self.calls = calls

    def plan(self, question: str, allowed_tools: tuple[str, ...]) -> list[ToolInvocation]:
        return self.calls


def test_agent_executes_allowlisted_tool_and_audits() -> None:
    audit = MemoryAuditSink()
    registry = ToolRegistry([
        ToolDefinition("github.list_files", "read", lambda args: {"files": ["README.md"]})
    ])
    agent = ControlledAgent(
        Planner([ToolInvocation("github.list_files", {"repository": "owner/repo", "ref": "main"})]),
        registry,
        audit,
    )
    results = agent.run("What files exist?")
    assert results[0].output["files"] == ["README.md"]
    assert audit.events[0]["outcome"] == "success"


def test_agent_enforces_tool_call_budget() -> None:
    registry = ToolRegistry([
        ToolDefinition("safe.read", "read", lambda args: {})
    ])
    calls = [ToolInvocation("safe.read", {}) for _ in range(6)]
    with pytest.raises(ValueError, match="budget"):
        ControlledAgent(Planner(calls), registry, MemoryAuditSink()).run("question")
