BASE_62_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def _validate_rank(rank: str) -> None:
    if isinstance(rank, str):
        if rank == "":
            raise ValueError("rank must not be empty string.")

        if rank == "00":
            raise ValueError("Unacceptable rank.")

        if len(rank) < 2:
            raise ValueError("rank must contain at least two digits.")

        if len(rank) > 2:
            if rank[-1] == "0":
                raise ValueError("rank must not end on zero.")

        for digit in rank:
            if digit not in BASE_62_DIGITS:
                raise ValueError(f"{rank} digit {digit} not in base62.")

    else:
        raise TypeError("rank must be str.")


def _rank_to_int(rank: str) -> int:
    rank_value = 0

    for digit in rank:
        digit_index = BASE_62_DIGITS.index(digit)
        rank_value = rank_value * 62 + digit_index

    return rank_value


def _int_to_base62(rank_value: int, width: int) -> str:
    new_rank = ""
    remaining_value = rank_value

    while remaining_value != 0:
        remaining_value, digit_index = divmod(remaining_value, 62)
        new_rank += BASE_62_DIGITS[digit_index]

    return new_rank[::-1].rjust(width, "0")


def rank_between(prev_rank: str | None, next_rank: str | None) -> str:

    if prev_rank is None and next_rank is None:
        return "a0"

    if prev_rank is not None:
        _validate_rank(prev_rank)

    if next_rank is not None:
        _validate_rank(next_rank)

    if prev_rank is not None and next_rank is not None:
        if prev_rank >= next_rank:
            raise ValueError("prev_rank must be less than next_rank.")

        width = max(len(prev_rank), len(next_rank)) + 1
        padded_prev_rank = prev_rank.ljust(width, "0")
        padded_next_rank = next_rank.ljust(width, "0")

        middle_int = (_rank_to_int(padded_prev_rank) + _rank_to_int(padded_next_rank)) // 2
        new_rank = _int_to_base62(middle_int, width)

        while new_rank[-1] == "0" and len(new_rank) > 2:
            new_rank = new_rank[:-1]

        if new_rank <= prev_rank or new_rank >= next_rank:
            raise ValueError("new_rank must be less than next_rank and higher than prev_rank.")

        _validate_rank(new_rank)

        return new_rank

    if prev_rank is None and next_rank is not None:
        next_rank = next_rank + "0"
        width = len(next_rank)

        midpoint_value = _rank_to_int(next_rank) // 2
        new_rank = _int_to_base62(midpoint_value, width)

        while new_rank[-1] == "0" and len(new_rank) > 2:
            new_rank = new_rank[:-1]

        if new_rank >= next_rank:
            raise ValueError("new_rank must be less than next_rank.")

        _validate_rank(new_rank)

        return new_rank

    if prev_rank is not None and next_rank is None:
        new_rank = prev_rank + "V"

        if new_rank <= prev_rank:
            raise ValueError("new_rank must be higher than prev_rank.")

        _validate_rank(new_rank)

        return new_rank


def rank_first(existing_first: str | None) -> str:
    return rank_between(prev_rank=None, next_rank=existing_first)


def rank_last(existing_last: str | None) -> str:
    return rank_between(prev_rank=existing_last, next_rank=None)
