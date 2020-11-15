import itertools
import random
from pprint import pprint

from statistics import mean, median

M = 4  # code length
N = 7  # number of colors
ALLOW_REPEATS = True  # allow repeated colors in code

if ALLOW_REPEATS:
    POOL = tuple(itertools.product(range(N), repeat=M))
else:
    POOL = tuple(itertools.permutations(range(N), r=M))


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


def test():
    # pick a code at random
    code = random.choice(POOL)
    # pools starts with all possible codes
    current_pool = POOL
    # let's keep track of each turn
    turns = []
    response = (0, 0)
    # when the pool gets down to 1, we know the code
    while response[0] < M:
        # make a random guess out of the current pool
        guess = random.choice(current_pool)
        # see how we did, and keep track of the result
        response = check_guess(code, guess)
        turns.append({"guess": guess, "response": response, "pool": len(current_pool)})
        # pare down the pool using the latest response
        current_pool = [
            code for code in current_pool if check_guess(code, guess) == response
        ]
    # double check we got it right
    assert current_pool[0] == code
    return {"code": code, "turns": turns}


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
    print(len(POOL))
    pprint(test())
