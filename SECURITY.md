# Security Policy

SentinelRAG treats repository content, retrieved text, model output, and tool arguments as untrusted data.

## Core boundaries

- Repository content must never be treated as trusted system instructions.
- Secrets belong in environment or deployment secret stores and must not be committed.
- Tool execution will use explicit allowlists and least privilege.
- High-impact repository mutations require human approval.
- Retrieved evidence must be cited before an answer is represented as grounded.

Please report security issues privately to the repository owner rather than opening a public exploit report.
