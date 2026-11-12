import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from api.ranking import ranks
from api.ranking.ranks import rank_between, rank_first, rank_last

CARD_COUNT = 10
MOVE_COUNT = 200

valid_rank_cases = st.text(
    alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    min_size=2,
    max_size=10,
).filter(lambda rank: rank[-1] != "0" if len(rank) > 2 else rank != "00")


@st.composite
def generated_ranks_order(draw) -> tuple[str, str]:
    first_rank = draw(valid_rank_cases)
    second_rank = draw(valid_rank_cases)

    assume(first_rank != second_rank)

    prev_rank, next_rank = sorted((first_rank, second_rank))

    return prev_rank, next_rank


@given(generated_ranks_order())
def test_generated_ranks(ranks) -> None:
    prev_rank, next_rank = ranks
    new_rank = rank_between(prev_rank, next_rank)

    assert len(new_rank) >= 2
    if len(new_rank) > 2:
        assert new_rank[-1] != "0"
    else:
        assert new_rank != "00"

    assert new_rank > prev_rank
    assert new_rank < next_rank


def test_move_card_to_end() -> None:
    ranks = {"A": "a0", "B": "a1", "C": "a2", "D": "a3"}
    expected_order = ["A", "C", "D", "B"]

    new_rank = rank_last(ranks["D"])
    ranks["B"] = new_rank

    actual_order = sorted(ranks, key=lambda card_id: ranks[card_id])
    assert actual_order == expected_order


def test_move_card_to_middle() -> None:
    ranks = {"A": "a0", "B": "a1", "C": "a2", "D": "a3"}
    expected_order = ["A", "D", "B", "C"]

    new_rank = rank_between(ranks["A"], ranks["B"])
    ranks["D"] = new_rank

    actual_order = sorted(ranks, key=lambda card_id: ranks[card_id])
    assert actual_order == expected_order


def test_move_card_to_beginning() -> None:
    ranks = {"A": "a0", "B": "a1", "C": "a2", "D": "a3"}
    expected_order = ["C", "A", "B", "D"]

    new_rank = rank_first(ranks["A"])
    ranks["C"] = new_rank

    actual_order = sorted(ranks, key=lambda card_id: ranks[card_id])
    assert actual_order == expected_order


@st.composite
def generate_move_insert_pos(draw, card_count: int) -> tuple[int, int]:
    moving_pos = draw(st.integers(min_value=0, max_value=card_count - 1))
    insertion_pos = draw(st.integers(min_value=0, max_value=card_count - 2))

    if insertion_pos >= moving_pos:
        insertion_pos += 1

    return moving_pos, insertion_pos


@given(
    initial_ranks=st.lists(
        valid_rank_cases,
        min_size=CARD_COUNT,
        max_size=CARD_COUNT,
        unique=True,
    ),
    moves=st.lists(
        generate_move_insert_pos(CARD_COUNT),
        min_size=MOVE_COUNT,
        max_size=MOVE_COUNT,
    ),
)
def test_various_card_movement(
    initial_ranks: list[str],
    moves: list[tuple[int, int]],
) -> None:
    ranks = dict(enumerate(sorted(initial_ranks)))
    expected_order = list(range(CARD_COUNT))
    actual_order = sorted(ranks, key=lambda card_id: ranks[card_id])

    for step, (moving_pos, insertion_pos) in enumerate(moves, start=1):
        expected_card = expected_order.pop(moving_pos)
        expected_order.insert(insertion_pos, expected_card)

        moving_card = actual_order.pop(moving_pos)

        if insertion_pos == 0:
            first_card = actual_order[0]
            new_rank = rank_first(ranks[first_card])
        elif insertion_pos == len(actual_order):
            last_card = actual_order[-1]
            new_rank = rank_last(ranks[last_card])
        else:
            remaining_cards = iter(actual_order)
            for _ in range(insertion_pos - 1):
                next(remaining_cards)

            left_card = next(remaining_cards)
            right_card = next(remaining_cards)
            new_rank = rank_between(ranks[left_card], ranks[right_card])

        ranks[moving_card] = new_rank
        actual_order = sorted(ranks, key=lambda card_id: ranks[card_id])

        assert len(set(ranks.values())) == CARD_COUNT, f"Duplicate rank at move {step}"
        assert actual_order == expected_order, (
            f"Move {step}: card {moving_card} from {moving_pos} to {insertion_pos}"
        )


@pytest.mark.parametrize(
    ("rank", "expected_error"),
    [
        ("", ValueError),
        ("00", ValueError),
        ("a", ValueError),
        ("a30", ValueError),
        ("a!", ValueError),
        (123, TypeError),
    ],
)
def test_rank_between_rejects_invalid_rank(
    rank: str | None, expected_error: type[ValueError] | type[TypeError]
) -> None:

    with pytest.raises(expected_error):
        rank_between(rank, None)


# tests for invalid calculation results
def test_rank_between_rejects_bad_result(monkeypatch):
    monkeypatch.setattr(ranks, "_int_to_base62", lambda value, width: "a3")

    with pytest.raises(ValueError):
        ranks.rank_between("a3", "a5")


def test_rank_first_rejects_bad_result(monkeypatch):
    monkeypatch.setattr(ranks, "_int_to_base62", lambda value, width: "b0")

    with pytest.raises(ValueError):
        ranks.rank_first("a5")
