
BASE_62_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def rank_between(prev_rank: str | None, next_rank: str | None) -> str:

    if prev_rank is not None and next_rank is not None:
        if isinstance(prev_rank, str) and isinstance(next_rank, str):

            for i in prev_rank:
                if i not in BASE_62_DIGITS:
                    raise ValueError(f"prev_rank digit {i} not in base62.")

            for i in next_rank:
                if i not in BASE_62_DIGITS:
                    raise ValueError(f"next_rank digit {i} not in base62.")

            if prev_rank >= next_rank:
                raise ValueError("prev_rank must be strictly less than next_rank.")
        else:
            raise ValueError("prev_rank and next_rank must both be str.")


    if prev_rank is None and next_rank is None:
        return "a0"

    if prev_rank is None and next_rank is not None:
        if isinstance(next_rank, str):

            for i in next_rank:
                if i not in BASE_62_DIGITS:
                    raise ValueError(f"next_rank digit {i} not in base62.")

        last_digit = next_rank[-1]

            digit_index = BASE_62_DIGITS.index(last_digit)

            if digit_index != 0:
                lower_digit = BASE_62_DIGITS[digit_index-1]
                new_rank = next_rank[:-1] + lower_digit

            else:
                new_rank, next_rank = next_rank, next_rank + BASE_62_DIGITS[31]

        else:
            raise ValueError

    return new_rank



def rank_first(existing_first: str) -> str:
    return rank_between(prev_rank=None, next_rank=existing_first)

def rank_last(existing_last: str) -> str:
    return rank_between(prev_rank=existing_last, next_rank=None)




