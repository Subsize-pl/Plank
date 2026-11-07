import pytest

from api.ranking.ranks import rank_between

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def assert_valid_rank(rank: str) -> None:
    assert isinstance(rank, str)
    assert len(rank) >= 2
    assert rank != "00"
    assert all(character in ALPHABET for character in rank)

    if len(rank) > 2:
        assert not rank.endswith("0")


@pytest.mark.parametrize(
    ("prev_rank", "next_rank", "expected"),
    [
        pytest.param(None, None, "a0", id="empty-list"),
        pytest.param(None, "a5", None, id="before-first"),
        pytest.param("a5", None, None, id="after-last"),
        pytest.param("a3", "a5", "a4", id="room-between"),
        pytest.param("a3", "a4", "a3V", id="adjacent-ranks"),
        pytest.param("a3V", "a3W", None, id="deep-ranks"),
        pytest.param("a0V", "a1V", "a1", id="remove-multiple-zeros"),
        pytest.param("000001", "zzzzzz", "V0", id="preserve-minimum-length"),
        pytest.param(None, "01", "00V", id="before-smallest-two-digit-rank"),
        pytest.param(None, "a0", "I0", id="normalize-before-first"),
        pytest.param("01", "011", None, id="prefix-boundaries"),
    ],
)

def test_rank_between(
    prev_rank: str | None,
    next_rank: str | None,
    expected: str | None,
) -> None:

    result = rank_between(prev_rank, next_rank)

    assert_valid_rank(result)

    if expected is not None:
        assert result == expected

    if prev_rank is not None:
        assert prev_rank < result

    if next_rank is not None:
        assert result < next_rank


@pytest.mark.parametrize(
    ("prev_rank", "next_rank"),
    [
        pytest.param("a3", "a3", id="equal-boundaries"),
        pytest.param("a5", "a3", id="reversed-boundaries"),
    ],
)

def test_rank_between_rejects_invalid_order(
    prev_rank: str,
    next_rank: str,
) -> None:

    with pytest.raises(ValueError, match="prev_rank must be less than next_rank"):
        rank_between(prev_rank, next_rank)
