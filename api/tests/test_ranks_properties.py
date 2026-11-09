from hypothesis import assume, strategies as st, given
from api.ranking.ranks import rank_between


valid_rank_cases = (
    st.text(
        alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        min_size=2,
        max_size=10,
    )
    .filter(
        lambda rank:rank [-1] != "0" if len(rank) > 2 else rank != "00"
    )
)

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

    assert new_rank > prev_rank and new_rank < next_rank


def test_move_card_to_end() -> None:
    ranks = {"A": "a0", "B": "a1", "C": "a2", "D": "a3"}
    expected_order = ["A", "C", "D", "B"]

    new_b_rank = rank_between(ranks["D"], None)
    ranks["B"] = new_b_rank

    ordered_ranks = sorted(ranks, key=lambda card_id: ranks[card_id])
    assert ordered_ranks == expected_order


def test_move_card_to_middle() -> None:
    ranks = {"A": "a0", "B": "a1", "C": "a2", "D": "a3"}
    expected_order = ["A", "D", "B", "C"]

    new_b_rank = rank_between(ranks["A"], ranks["B"])
    ranks["D"] = new_b_rank

    ordered_ranks = sorted(ranks, key=lambda card_id: ranks[card_id])
    assert ordered_ranks == expected_order


def test_move_card_to_beginning() -> None:
    ranks = {"A": "a0", "B": "a1", "C": "a2", "D": "a3"}
    expected_order = ["C", "A", "B", "D"]

    new_b_rank = rank_between(None, ranks["A"])
    ranks["C"] = new_b_rank

    ordered_ranks = sorted(ranks, key=lambda card_id: ranks[card_id])
    assert ordered_ranks == expected_order
