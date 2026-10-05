from dataclasses import dataclass
from typing import Any, Callable, Mapping


class ToolError(ValueError):
    pass


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    handler: Callable[[Mapping[str, Any]], Mapping[str, Any]]
    read_only: bool = True


@dataclass(frozen=True)
class ToolInvocation:
    name: str
    arguments: Mapping[str, Any]


@dataclass(frozen=True)
class ToolResult:
    name: str
    output: Mapping[str, Any]


class ToolRegistry:
    def __init__(self, tools: list[ToolDefinition]) -> None:
        if any(not tool.read_only for tool in tools):
            raise ToolError("SentinelRAG agents may register read-only tools only")
        self._tools = {tool.name: tool for tool in tools}

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def invoke(self, invocation: ToolInvocation) -> ToolResult:
        tool = self._tools.get(invocation.name)
        if tool is None:
            raise ToolError(f"Tool is not allowlisted: {invocation.name}")
        return ToolResult(name=tool.name, output=tool.handler(invocation.arguments))
