import pytest

from sentinel_rag.costs import ModelPrice, estimate_cost


def test_cost_estimate_uses_token_direction() -> None:
    price = ModelPrice(input_per_million=1.0, output_per_million=2.0)
    assert estimate_cost(1_000_000, 500_000, price) == 2.0


def test_negative_tokens_are_rejected() -> None:
    with pytest.raises(ValueError):
        estimate_cost(-1, 0, ModelPrice(1.0, 1.0))
