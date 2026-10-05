from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPrice:
    input_per_million: float
    output_per_million: float


def estimate_cost(input_tokens: int, output_tokens: int, price: ModelPrice) -> float:
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts cannot be negative")
    return (
        input_tokens * price.input_per_million / 1_000_000
        + output_tokens * price.output_per_million / 1_000_000
    )
