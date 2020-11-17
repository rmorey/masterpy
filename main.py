import itertools
import random
from pprint import pprint
import numpy as np

from statistics import mean, median

M = 4  # code length
N = 7  # number of colors
ALLOW_REPEATS = True  # allow repeated colors in code

if ALLOW_REPEATS:
    POOL = tuple(itertools.product(range(N), repeat=M))
else:
    POOL = tuple(itertools.permutations(range(N), r=M))


def print_return(obj):
    print(obj)
    return obj


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


def get_random_code():
    return tuple(random.choice(range(N)) for _ in range(M))


def get_best_guess(turns):
    best = turns[0]
    best_n = 0
    for turn in turns:
        n = sum(turn["response"])
        if n > best_n:
            best = turn["guess"]
            best_n = n

    return best


def test(code=None):
    if code is None:
        code = random.choice(POOL)
    current_pool = POOL
    turns = []
    response = (-1, -1)
    while response[0] < M:
        guess = random.choice(current_pool)
        response = check_guess(code, guess)
        print(f"{guess=}, {response=}")

        turns.append({"guess": guess, "response": response, "pool": len(current_pool)})
        print(get_best_guess(turns))
        current_pool = [
            code for code in current_pool if check_guess(code, guess) == response
        ]
    # double check we got it right
    assert current_pool[0] == code
    return {"code": code, "turns": turns}


def sim(c1, c2):
    return sum([a == b for a, b in zip(c1, c2)])


def test4(code=None):
    if code is None:
        code = random.choice(POOL)
    current_pool = list(POOL)
    turns = []
    response = (-1, -1)
    best_guess = random.choice(POOL)
    while response[0] < M:
        current_pool.sort(key=lambda c: sim(best_guess, c))
        guess = current_pool[-1]
        response = check_guess(code, guess)
        print(f"{guess=}, {response=}")

        turns.append({"guess": guess, "response": response, "pool": len(current_pool)})
        print(get_best_guess(turns))
        current_pool = [
            code for code in current_pool if check_guess(code, guess) == response
        ]
    # double check we got it right
    assert current_pool[0] == code
    return {"code": code, "turns": turns}


def test2():
    # select code from the full pool at random
    code = random.choice(POOL)
    # let's keep track of each turn
    turns = []

    response = (-1, -1)
    dont_try = []
    while response[0] < M:
        # make a random guess out of the current pool
        done = False
        while not done:

            guess = get_random_code()
            while guess in dont_try:
                guess = get_random_code()

            print(f"Should I try: {guess}?")
            done = True
            for turn in turns:
                if check_guess(guess, turn["guess"]) != turn["response"]:
                    dont_try.append(guess)
                    print(f"nope, doesn't match: {turn}")
                    done = False
                    break
                else:
                    continue
            if done:
                print(f"{guess} looks good")
                break
        # see how we did, and keep track of the result
        response = check_guess(code, guess)
        turns.append({"guess": guess, "response": response})
    # double check we got it right
    assert guess == code
    result = {"code": code, "turns": turns}
    return result


def test3():
    code = random.choice(POOL)
    turns = []
    response = (-1, -1)
    while response[0] < M:
        guess = get_random_code()
        response = check_guess(code, guess)
        turns.append({"guess": guess, "response": response})
    assert guess == code
    result = {"code": code, "turns": turns}
    return result


def test_stats(n=len(POOL)):
    print("Testing...")
    results = [test() for _ in range(n)]
    n_guesses = [len(r["turns"]) for r in results]
    print(
        f"{n=}, {mean(n_guesses)=:.2f}, {median(n_guesses)=}, {max(n_guesses)=}, {min(n_guesses)=}"
    )


def play():
    # play against the computer as codebreaker
    code = random.choice(POOL)
    print("I have a code set")
    guesses = 0
    while True:
        guesses += 1
        guess = eval(input(f"Guess # {guesses}? "))
        hits, blows = check_guess(code, guess)
        if hits == M:
            print("that's right!")
            print(f"{guesses}")
            exit()
        else:
            print(f"{hits} Hits and {blows} Blows")


def play_master():
    # play against the computer as codemaster
    current_pool = POOL
    guesses = 0
    print("Ready? ", end="")
    while len(current_pool) > 1:
        guesses += 1
        guess = random.choice(current_pool)
        print(f"My guess is: {guess}")
        hits = int(input("Hits? "))
        blows = int(input("Blows? "))
        if hits == M:
            print(f"I got it in {guesses}!")
            exit()
        else:
            current_pool = [
                code
                for code in current_pool
                if check_guess(code, guess) == (hits, blows)
            ]

    print(f"I know! It's {current_pool[0]}")


if __name__ == "__main__":
    print(sorted(POOL, key=lambda c: sim((1, 2, 3, 4), c)))
