
BASE_62_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def _validate_rank(rank: str) -> None:
    if isinstance(rank, str):
        if rank == "":
            raise ValueError("rank must not be empty string.")

        if len(rank) >= 2:
            if rank[-1] == "0":
                raise ValueError("rank must not end on zero.")
        else:
            raise ValueError("rank must contain at least two digits.")

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


def _int_to_base62(rank_value: int) -> str:
    new_rank = ""
    cur_value = rank_value

    while cur_value != 0:
        cur_value, digit_index = divmod(cur_value, 62)
        new_rank += BASE_62_DIGITS[digit_index]

    return new_rank[::-1]



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
        raise NotImplementedError

    if prev_rank is None and next_rank is not None:



        last_digit = next_rank[-1]
        digit_index = BASE_62_DIGITS.index(last_digit)

        if digit_index != 0:
            new_rank = next_rank[:-1] + BASE_62_DIGITS[digit_index - 1]
        else:
            if len(next_rank) >= 2:
                pre_last_digit_index = BASE_62_DIGITS.index(next_rank[-2])
                new_rank = next_rank[::-2] + BASE_62_DIGITS[pre_last_digit_index:1:-1] + BASE_62_DIGITS[-1]
            else:
                raise NotImplementedError



    if prev_rank is not None and next_rank is None:
        raise NotImplementedError



    #     last_digit = next_rank[-1]
    #
    #         digit_index = BASE_62_DIGITS.index(last_digit)
    #
    #             if digit_index != 0:
    #                 lower_digit = BASE_62_DIGITS[digit_index-1]
    #                 new_rank = next_rank[:-1] + lower_digit
    #
    #             else:
    #                 new_rank, next_rank = next_rank, next_rank + BASE_62_DIGITS[31]
    #
    #     else:
    #         raise ValueError
    #
    return new_rank



def rank_first(existing_first: str) -> str:
    return rank_between(prev_rank=None, next_rank=existing_first)

def rank_last(existing_last: str) -> str:
    return rank_between(prev_rank=existing_last, next_rank=None)




