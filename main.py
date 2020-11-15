import itertools
import random
from collections import namedtuple
from random import choice
import logging
from statistics import mean, median
import click
from pprint import pprint

M = 4  # code size
N = 7  # number of colors
ALLOW_REPEATS = True  # allow repeats in code

logging.basicConfig(level=logging.WARNING)


if ALLOW_REPEATS:
    POOL = tuple(itertools.product(range(N), repeat=M))
else:
    POOL = tuple(itertools.permutations(range(N), r=M))

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


def get_rand_code(pool=POOL):
    return choice(pool)


def get_first_code(pool=POOL):
    return pool[0]


def get_last_code(pool=POOL):
    return pool[-1]


def get_updated_pool(pool, guess, resp):
    return tuple(code for code in pool if check_guess(code, guess) == resp)


def test(n=1, strategy=get_rand_code):
    games = []
    for _ in range(n):
        code = get_rand_code(POOL)
        game = {"code": code, "turns": []}
        pool = POOL
        while len(pool) > 1:
            guess = strategy(pool)
            hits, blows = check_guess(code, guess)
            pool = get_updated_pool(pool, guess, (hits, blows))

            game["turns"].append(
                {"guess": guess, "resp": (hits, blows), "new_pool_len": len(pool)}
            )
        assert pool[0] == code
        games.append(game)
    return games


def play():
    code = get_rand_code()
    print("I have a code set")
    guesses = 0
    while True:
        guesses += 1
        guess = eval(input(f"Guess # {guesses}? "))
        resp = check_guess(code, guess)
        if resp.hits == M:
            print("that's right!")
            print(f"{guesses}")
            exit()
        else:
            print(f"{resp.hits} Hits and {resp.blows} Blows")


def play_master(strat=get_rand_code):
    pool = POOL
    guesses = 0
    print("Ready? ", end="")
    while len(pool) > 1:
        guess = strat(pool)
        guesses += 1
        print(f"My guess is: {guess}")
        hits = int(input("Hits? "))
        blows = int(input("Blows? "))
        if hits == 4:
            print(f"I got it in {guesses}!")
            exit()
        else:
            pool = get_updated_pool(pool, guess, (hits, blows))

    print(f"I know! It's {pool[0]}")


def test_strats(n=100):

    strats = [get_rand_code, get_first_code, get_last_code]
    for strat in strats:
        test_strat(n, strat)


def test_strat(strat, n=100):
    results = test(n, strategy=strat)
    print(strat.__name__)
    n_guesses = [len(r["turns"]) for r in results]
    print(
        f"{mean(n_guesses)=},{median(n_guesses)=},{max(n_guesses)=},{min(n_guesses)=}"
    )
    print()


if __name__ == "__main__":
    test_strat(get_rand_code)
