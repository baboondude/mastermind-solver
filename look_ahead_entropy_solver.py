# GENERALIZED - The look-ahead entropy algorithm
# guess_number() makes the computer play as the guesser against human
# guess_number_sim() simulates whatever you want it to and prints results

import math
import random

ALPHABET_SIZE = 8
WORD_LEN = 5

RANDOMIZATION = True

SIMULATION = False
FILENAME = "results.csv"


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


def create_entropy_dist(all, poss):
    entropy_dist_dict = {}
    for pot_guess in all:
        score_dict = {}
        for pot_num in poss:
            score = score_guess(pot_guess, pot_num)
            if score not in score_dict:
                score_dict[score] = 1
            else:
                score_dict[score] = score_dict[score] + 1

        for key in score_dict:
            score_dict[key] = float(score_dict[key])/len(poss)

        entropy_dist_dict[pot_guess] = entropy_of_dist(score_dict.values())

    return entropy_dist_dict


def entropy_of_val(prob):
    if prob != 0:
        return math.log((1.0 / prob), 2)
    else:
        return 0.0


def entropy_of_dist(prob_dist):
    entropy = 0.0
    for prob in prob_dist:
        entropy += prob * entropy_of_val(prob)

    return entropy


def guess_number():

    guess_set = []
    poss = []

    for i in range(0, 10**WORD_LEN):
        i = str(i)
        i = "0" * (WORD_LEN - len(i)) + i
        if check_diff_digits(i) and valid_digits(i):
            guess_set.append(i)
            poss.append(i)

    print("Random Number for your convenience:", poss[random.randint(0, len(poss) - 1)])

    guess = "0"
    # 0 = no digits correct
    # 1 = one digit correct out of place
    # 2 = one digit correct in place
    score = "0"

    num_guesses = 0

    while score != "2"*WORD_LEN:

        print("Possibilities:\t", poss)

        if len(poss) == len(guess_set) or len(poss) == 1:
            if RANDOMIZATION:
                guess = poss[random.randint(0, len(poss) - 1)]
            else:
                guess = poss[0]
        elif len(poss) > 1:
            dist = create_entropy_dist(guess_set, poss)
            print(dist)
            max_val = 0
            guess = poss[0]
            for tup in dist.items():
                if tup[1] > max_val:
                    max_val = tup[1]
                    guess = tup[0]
        else:
            guess = None
            print("No possibilities left. Please check all previous scorings for errors.")
            exit(1)

        print("My guess is", guess)

        if WORD_LEN == 5 and ALPHABET_SIZE == 8:
            for c in guess:
                if c == '0':
                    print("Pink ", end='')
                elif c == '1':
                    print("Red ", end='')
                elif c == '2':
                    print("Orange ", end='')
                elif c == '3':
                    print("Yellow ", end='')
                elif c == '4':
                    print("Green ", end='')
                elif c == '5':
                    print("Blue ", end='')
                elif c == '6':
                    print("Purple ", end='')
                elif c == '7':
                    print("White ", end='')

        response = input("\nEnter score:\n").split()

        score = response[0]

        num_guesses += 1

        poss = eliminate_poss(guess, score, poss)

    print("It took me %d guesses" % num_guesses)
    return


def guess_number_sim():

    all_nums = []
    for i in range(0, 10 ** WORD_LEN):
        i = str(i)
        i = "0" * (WORD_LEN - len(i)) + i
        if check_diff_digits(i) and valid_digits(i): # and random.randint(0, 66) == 0:
            all_nums.append(i)

    arr_guesses = []

    for actual in all_nums:
        print(actual)
        guess_set = []
        poss = []

        for i in range(0, 10 ** WORD_LEN):
            i = str(i)
            i = "0" * (WORD_LEN - len(i)) + i
            if check_diff_digits(i) and valid_digits(i):
                guess_set.append(i)
                poss.append(i)

        guess = "0"
        # 0 = no digits correct
        # 1 = one digit correct out of place
        # 2 = one digit correct in place
        score = "0"

        num_guesses = 0
        while score != "2" * WORD_LEN:

            # print("Possibilities:\t", poss)

            if len(poss) == len(guess_set) or len(poss) == 1:
                guess = poss[random.randint(0, len(poss) - 1)]
            elif len(poss) > 1:
                dist = create_entropy_dist(guess_set, poss)
                # print(dist)
                max_val = 0
                guess = poss[0]
                for tup in dist.items():
                    if tup[1] > max_val:
                        max_val = tup[1]
                        guess = tup[0]
            else:
                guess = None
                print("No possibilities left. Please check all previous scorings for errors.")
                exit(1)

            score = score_guess(actual, guess)
            num_guesses += 1
            poss = eliminate_poss(guess, score, poss)

        arr_guesses.append(num_guesses)

    return arr_guesses


if SIMULATION:
    arr = guess_number_sim()
    fh = open(FILENAME, 'w')
    fh.write(str(arr))
    fh.close()
else:
    guess_number()
