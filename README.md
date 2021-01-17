# mastermind-solver
Solver and playable interface for games such as Mastermind. Loosely based on information-theoretic ideas.

## Rules
Games such as Bagel and Mastermind are based on guessing a specific digit-pattern (all unique) from a given alphabet of digits. 

There are two players in the game: the Scorer (S) and the Guesser (G). The game begins with the Scorer setting a digit-pattern of length WORD_LEN from an alphabet of digits of size ALPHABET_SIZE, both quantities known in advance by the Guesser. The game then continues with the Guesser positing queries and the Scorer responding with a score for each one. 

Each query must represent a valid digit-pattern under ALPHABET_SIZE and WORD_LEN, with all unique digits. To score a query, the Scorer awards:
- a '0' for each digit in the query that doesn't appear at all in the preset pattern,
- a '1' for each query-digit that appears in a different position in the preset pattern, and
- a '2' for each query-digit that appears in the same position as it does in the preset pattern. 

The order of digits in the score does not correspond to the order of digits. For this code, the score is presented with 0s first, followed by 1s and then 2s. This query-score pattern continues until the Guesser guesses the correct digit-pattern. The guesses may not match the information given so far, but they do have to contain unique digits from the Alphabet and must be of the predecided length. The objective of the guesser is to minimize NUM_GUESSES for each game. 

**Restrictions:**
- ALPHABET_SIZE <= 10
- WORD_LEN <= ALPHABET_SIZE

**Common Configurations:**
- Mastermind: 
  - ALPHABET_SIZE = 8
  - WORD_LEN = 5
 
- Bagel: 
  - ALPHABET_SIZE = 10
  - WORD_LEN = 3

## Algorithm
The code contains three potential algorithms to play the game. 

The first algorithm represents a primitive algorithm that maintains a list of valid digit-patterns following each score, and simply guesses a randomly-selected valid pattern with each query. 

The second algorithm contains a flawed information-theoretic implementation. This algorithm also maintains a list of valid digit-patterns following each score. From that list, it then generates a probability distribution for how often each digit appears in each position. For instance, for Bagel, this configuration would be stored in a 10x3 matrix. It then 'grades' each valid digit-pattern by taking the sum of the relative entropy of each digit by calculating h(x) = log(1/p) for each digit-position probability. The number-sequence with the highest probability is then guessed. This algorithm presents a problem in that it doesn't consider that placing a digit out-of-position also often yields valuable information. Furthermore, it is rather suspiciously formulated in terms of information theory. 

The third algorithm maintains a list of valid-digit-patterns following each score as well as the initial list of valid patterns constrained by only the ALPHABET_SIZE and WORD_LEN parameters. With each score, it evaluates the entropy of each potential guess — which could be any pattern-sequence in the initial list — by evaluating the probability distribution of the potential scores that the query could yield based on the list of valid-digit-patterns. The entropy of each probability-distribution is then evaluated, and the query that maximizes entropy is posited to the Scorer. Although far more computationally intensive than other algorithms, this virtually eliminates NUM_GUESSES passing over a certain threshold. 

## TODO
- Implement a fourth algorithm that incorporates the look-ahead strategy of Algorithm 3 and looks ahead more than one move to calculate sub-entropies. Although far more computationally intensive, some sort of random sampling may prove sufficiient to estimate the entropy rather than a full calculation. 
- Print the expected/actual number of bits of information gained per guess, as well as the amount of information each game contains at the start. 

## Simulation Data
The following spreadsheet contains data for simulations of Bagel and Mastermind using the three algorithms. 
https://docs.google.com/spreadsheets/d/1Ebnig9PpTZ8JUQZorNNzVFcffMRxEXCH0bY07eGA6i4/edit#gid=798220679
*The fourth algorithm included in the Bagel data simply represents the third algorithm with the first guess randomized. This random-version, although not used
for Mastermind testing, represents the default version moving forward.*
