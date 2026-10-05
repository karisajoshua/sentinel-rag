from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class AuditEvent:
    timestamp: str
    event: str
    tool: str
    arguments: Mapping[str, Any]
    outcome: str


class AuditSink(Protocol):
    def record(self, event: AuditEvent) -> None: ...


class MemoryAuditSink:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def record(self, event: AuditEvent) -> None:
        self.events.append(asdict(event))


def audit_event(tool: str, arguments: Mapping[str, Any], outcome: str) -> AuditEvent:
    return AuditEvent(
        timestamp=datetime.now(UTC).isoformat(),
        event="tool_invocation",
        tool=tool,
        arguments=dict(arguments),
        outcome=outcome,
    )
