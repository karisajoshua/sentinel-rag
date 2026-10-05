from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Iterator

from opentelemetry import metrics, trace


tracer = trace.get_tracer("sentinel_rag")
meter = metrics.get_meter("sentinel_rag")
request_latency = meter.create_histogram("sentinel_rag.request.duration", unit="ms")
llm_tokens = meter.create_counter("sentinel_rag.llm.tokens", unit="{token}")
estimated_cost = meter.create_counter("sentinel_rag.llm.estimated_cost", unit="USD")


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


def record_usage(usage: Usage, model: str) -> None:
    attributes = {"model": model}
    llm_tokens.add(usage.input_tokens, {**attributes, "direction": "input"})
    llm_tokens.add(usage.output_tokens, {**attributes, "direction": "output"})
    estimated_cost.add(usage.estimated_cost_usd, attributes)


@contextmanager
def operation_span(name: str) -> Iterator[None]:
    start = perf_counter()
    with tracer.start_as_current_span(name):
        try:
            yield
        finally:
            request_latency.record((perf_counter() - start) * 1000, {"operation": name})
