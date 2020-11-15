from collections import namedtuple
from itertools import product, permutations
from random import choice

M = 4  # code size
N = 7  # number of colors
REPEATS = True  # allow repeats in code


if REPEATS:
    POOL = tuple(product(range(N), repeat=M))
else:
    POOL = tuple(permutations(range(N), r=M))

Response = namedtuple("Result", ("hits", "blows"))


def check_guess(code, guess):
    code, guess = list(code), list(guess)
    hits = blows = 0
    for i in range(M):
        c, g = code[i], guess[i]
        if g == c:
            code[i] = -1
            guess[i] = -2
            hits += 1
    for i in range(M):
        g = guess[i]
        if g in code:
            code.remove(g)
            guess[i] = -2
            blows += 1
    return Response(hits, blows)


def get_rand_code():
    return choice(POOL)


def check_rand_pair():
    code = get_rand_code()
    guess = get_rand_code()
    hits, blows = check_guess(code, guess)
    print(f"{code=}")
    print(f"{guess=}")
    print(f"{hits=},{blows=}")


def get_updated_pool(pool, guess, resp):
    return tuple(code for code in pool if check_guess(code, guess) == resp)


if __name__ == "__main__":
    for _ in range(100):
        code1 = get_rand_code()
        guess1 = get_rand_code()
        print(f"{code1=},{guess1=}")
        new_pool = get_updated_pool(POOL, guess1, check_guess(code1, guess1))
        print(len(new_pool))
        assert code1 in new_pool
