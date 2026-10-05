from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from .audit import AuditSink, audit_event
from .tools import ToolInvocation, ToolRegistry, ToolResult


class ToolPlanner(Protocol):
    def plan(self, question: str, allowed_tools: Sequence[str]) -> list[ToolInvocation]: ...


@dataclass
class ControlledAgent:
    planner: ToolPlanner
    registry: ToolRegistry
    audit: AuditSink
    max_tool_calls: int = 5

    def run(self, question: str) -> list[ToolResult]:
        plan = self.planner.plan(question, self.registry.names)
        if len(plan) > self.max_tool_calls:
            raise ValueError("tool-call budget exceeded")

        results: list[ToolResult] = []
        for invocation in plan:
            try:
                result = self.registry.invoke(invocation)
            except Exception:
                self.audit.record(audit_event(invocation.name, invocation.arguments, "rejected-or-failed"))
                raise
            self.audit.record(audit_event(invocation.name, invocation.arguments, "success"))
            results.append(result)
        return results
