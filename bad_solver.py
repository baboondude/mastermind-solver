# GENERALIZED - Random guesses that could be true
# guess_number() makes the computer play as the guesser against human
# guess_number_sim() simulates whatever you want it to and prints results

import math
import random

ALPHABET_SIZE = 10
WORD_LEN = 3

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


def create_prob_dist(poss):
    dist = [[0] * WORD_LEN for i in range(ALPHABET_SIZE)]

    for num in poss:
        for c in range(0, WORD_LEN):
            dist[int(num[c])][c] += 1

    for r in range(ALPHABET_SIZE):
        for c in range(WORD_LEN):
            try:
                dist[r][c] /= float(len(poss))
            except ZeroDivisionError:
                print("No possibilities left.")
                exit(-1)

    return dist


def entropy_prob(prob):
    if prob != 0 and prob != 1:
        return prob * math.log(1.0 / prob, 2) + (1 - prob) * math.log(1.0 / (1 - prob), 2)
    else:
        return 0


def entropy_num(num, prob):
    entropy = 0.0
    for i in range(WORD_LEN):
        entropy += entropy_prob(prob[int(num[i])][i])

    return entropy


def guess_number():

    known_list = []
    poss = []
    dist = []

    for i in range(0, 10**WORD_LEN):
        i = str(i)
        i = "0" * (WORD_LEN - len(i)) + i
        if check_diff_digits(i) and valid_digits(i):
            known_list.append(i)
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
        dist = create_prob_dist(poss)
        print("Prob Dist:\t", dist)

        guess = ""
        if len(poss) > 1:
            known_entropies = [entropy_num(num, dist) for num in poss]
            guess = poss[known_entropies.index(max(known_entropies))]
        else:
            guess = poss[0]

        print("My guess is", guess)
        response = input("Enter score:\n").split()

        score = response[0]

        num_guesses += 1

        poss = eliminate_poss(guess, score, poss)
        # poss.remove(guess)

        # print(known_entropies)

    print("It took me %d guesses" % num_guesses)
    return


def guess_number_sim():

    all_nums = []
    for i in range(0, 10 ** WORD_LEN):
        i = str(i)
        i = "0" * (WORD_LEN - len(i)) + i
        if check_diff_digits(i) and valid_digits(i): # and random.randint(0, 11) == 0:
            all_nums.append(i)

    arr_guesses = []

    for actual in all_nums:
        known_list = []
        poss = []

        for i in range(0, 10 ** WORD_LEN):
            i = str(i)
            i = "0" * (WORD_LEN - len(i)) + i
            if check_diff_digits(i) and valid_digits(i):
                known_list.append(i)
                poss.append(i)

        guess = "0"
        # 0 = no digits correct
        # 1 = one digit correct out of place
        # 2 = one digit correct in place
        score = "0"

        num_guesses = 0
        while score != "2"*WORD_LEN:
            dist = create_prob_dist(poss)

            guess = poss[random.randint(0,len(poss)-1)]

            score = score_guess(actual, guess)

            num_guesses += 1

            poss = eliminate_poss(guess, score, poss)
            # poss.remove(guess)

            # print(known_entropies)

        arr_guesses.append(num_guesses)

    return arr_guesses


arr = guess_number_sim()

fh = open(FILENAME, 'w')
fh.write(str(arr))
fh.close()

# guess_number()