import random

M = 4  # code size
N = 6  # number of colors


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
    return hits, blows


def get_rand_code():
    return tuple(random.randint(0, N - 1) for _ in range(M))


def check_rand_pair():
    code1 = get_rand_code()
    guess1 = get_rand_code()
    hits, blows = check_guess(code1, guess1)
    print(f"{code1=}")
    print(f"{guess1=}")
    print(f"{hits=},{blows=}")


if __name__ == "__main__":
    for _ in range(10):
        check_rand_pair()
        print()
