# Evaluation and observability

SentinelRAG evaluates the retrieval and evidence chain separately from model fluency.

## Offline evaluation

Each case contains a question and the repository paths expected to contain supporting evidence. The current deterministic metrics are:

- retrieval hit rate
- mean reciprocal rank (MRR)
- citation coverage
- grounded-answer rate

These metrics are intentionally model-independent and suitable for CI regression tests.

## Runtime observability

OpenTelemetry instruments operation latency and LLM usage. Telemetry records operational metadata such as operation name, model identifier, token counts, and estimated cost.

Repository source text, retrieved chunks, prompts, secrets, and generated answers are **not telemetry attributes by default**. This reduces accidental disclosure through traces or metrics.

Pricing is supplied as data rather than hard-coded to a provider's current prices, so cost estimates remain testable and do not silently become stale.
