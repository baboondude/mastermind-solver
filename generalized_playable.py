# LETS YOU PLAY THE GAME AS THE GUESSER

import math
import random

ALPHABET_SIZE = 10
WORD_LEN = 3

PRINT_POSS = False


def check_diff_digits(num):
    return len(num) == len(set(num))


def valid_digits(num):
    for c in num:
        if int(c) >= ALPHABET_SIZE:
            return False

    return True


def score_guess(actual, guess):
    inter = ''.join(set(actual).intersection(set(guess)))

    ans = "0" * (WORD_LEN - len(inter))

    for c in inter:
        if actual.index(c) == guess.index(c):
            ans += "2"
        else:
            ans += "1"

    return ''.join(sorted(ans))


def eliminate_poss(guess, score, poss):
    new_poss = []

    for num in poss:
        if score_guess(guess, num) == score:
            new_poss.append(num)

    return new_poss


def guess_number():

    known_list = []
    poss = []

    for i in range(0, 10 ** WORD_LEN):
        i = str(i)
        i = "0" * (WORD_LEN - len(i)) + i
        if check_diff_digits(i):
            known_list.append(i)
            poss.append(i)

    actual = poss[random.randint(0, len(poss) - 1)]

    guess = "0"
    # 0 = no digits correct
    # 1 = one digit correct out of place
    # 2 = one digit correct in place
    score = "0"

    num_guesses = 0
    while score != "2"*WORD_LEN:
        if PRINT_POSS:
            print("Possibilities:\t", poss)

        response = input("Enter guess:\n").split()

        guess = response[0]
        score = score_guess(actual, guess)

        num_guesses += 1

        print("Score", score)

        poss = eliminate_poss(guess, score, poss)

    print("Number of guesses taken:", num_guesses)
    return


guess_number()
