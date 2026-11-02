
BASE_62_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def _validate_rank(rank: str) -> None:
    if isinstance(rank, str):
        if rank == "":
            raise ValueError("rank must not be empty string.")

        for digit in rank:
            if digit not in BASE_62_DIGITS:
                raise ValueError(f"{rank} digit {digit} not in base62.")

    else:
        raise ValueError("rank must be str.")



def rank_between(prev_rank: str | None, next_rank: str | None) -> str:

    if prev_rank is None and next_rank is None:
        return "a0"

    if prev_rank is not None:
        _validate_rank(prev_rank)

    if next_rank is not None:
        _validate_rank(next_rank)


    if prev_rank is None and next_rank is not None:


    if prev_rank is not None and next_rank is None:



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
    # return new_rank



def rank_first(existing_first: str) -> str:
    return rank_between(prev_rank=None, next_rank=existing_first)

def rank_last(existing_last: str) -> str:
    return rank_between(prev_rank=existing_last, next_rank=None)




