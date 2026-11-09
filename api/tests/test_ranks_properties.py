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
def ordered_ranks(draw):
    first_rank = draw(valid_rank_cases)
    second_rank = draw(valid_rank_cases)

    assume(first_rank != second_rank)

    prev_rank, next_rank = sorted((first_rank, second_rank))

    return prev_rank, next_rank


@given(ordered_ranks())
def test_generated_ranks(ranks):
    prev_rank, next_rank = ranks
    new_rank = rank_between(prev_rank, next_rank)

    assert len(new_rank) >= 2
    if len(new_rank) > 2:
        assert new_rank[-1] != "0"
    else:
        assert new_rank != "00"

    assert new_rank > prev_rank and new_rank < next_rank

