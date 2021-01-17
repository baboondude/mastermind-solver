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

## Usage
Run *look_ahead_entropy_solver.py* to have the computer play the Guesser and user play the Scorer. This file uses the third algorithm (see **Algorithm** section).
This file can also be configured to simulate a number of test cases by changing the parameters at the top of the code. 
Parameters:
- **ALPHABET_SIZE** (1 <= int <= 10)
  - The size of the alphabet, as explained in the rules (# of valid digits)
- **WORD_LEN** (1 <= int <= ALPHABET_SIZE)
  - The size of a digit-pattern. Must not exceed the size of the alphabet.
- **RANDOMIZATION** (True/False)
  - Whether to randomize the first guess. This should typically be True.
- **SIMULATION** (True/False)
  - Whether to run it in simulation mode. This should typically be False unless testing for efficiency. 
- **SIMULATION_FREQUENCY** (0.0 < float <= 1.0) 
  - If running a simulation, what fraction of possible digit sequences to actually test
  - Will be approximated using random() and checking if answer falls below SIMULATION_FREQUENCY
- **FILENAME** (string)
  - The output file for array of num_guesses data if running a simulation.

Run *generalized_playable.py* to have the computer play the Scorer and user play the Guesser. The computer will optionally print a list of possibilities (can be toggled with constant at top of code) to aid the user. 


## Algorithm
The code contains three potential algorithms to play the game, one of which is maintained and currently used.

The **first algorithm** represents a primitive algorithm that maintains a list of valid digit-patterns following each score, and simply guesses a randomly-selected valid pattern with each query. It is stored in file *Old\ Algorithms/bad_solver.py*.

The **second algorithm** contains a flawed information-theoretic implementation. This algorithm also maintains a list of valid digit-patterns following each score. From that list, it then generates a probability distribution for how often each digit appears in each position. For instance, for Bagel, this configuration would be stored in a 10x3 matrix. It then 'grades' each valid digit-pattern by taking the sum of the relative entropy of each digit by calculating h(x) = log(1/p) for each digit-position probability. The number-sequence with the highest probability is then guessed. This algorithm presents a problem in that it doesn't consider that placing a digit out-of-position also often yields valuable information. Furthermore, it is rather suspiciously formulated in terms of information theory. It is stored in file *Old\ Algorithms/digit_entropy_solver.py*. 

The **third algorithm, the main one** maintains a list of valid-digit-patterns following each score as well as the initial list of valid patterns constrained by only the ALPHABET_SIZE and WORD_LEN parameters. With each score, it evaluates the entropy of each potential guess — which could be any pattern-sequence in the initial list — by evaluating the probability distribution of the potential scores that the query could yield based on the list of valid-digit-patterns. The entropy of each probability-distribution is then evaluated, and the query that maximizes entropy is posited to the Scorer. Although far more computationally intensive than other algorithms, this virtually eliminates NUM_GUESSES passing over a certain threshold. It is stored in file *look_ahead_entropy_solver.py*. 
 
*Update 1/16/20 11:40 p.m: This algorithm now prioritizes guesses that fall within the evolving list of valid-digit-patterns if two guesses have the same entropy, vastly improving efficiency near the end of games. This yielded a significant change in the data and solidified this algorithm as far superior to the previous ones, as shown in the data spreadsheet below.*

## TODO
- Implement a fourth algorithm that incorporates the look-ahead strategy of Algorithm 3 and looks ahead more than one move to calculate sub-entropies. Although far more computationally intensive, some sort of random sampling may prove sufficiient to estimate the entropy rather than a full calculation. Stored in *Old\ Algorithms/look_ahead_multiple.py*

## Simulation Data
The following spreadsheet contains data for simulations of Bagel and Mastermind using the three algorithms. 
https://docs.google.com/spreadsheets/d/1Ebnig9PpTZ8JUQZorNNzVFcffMRxEXCH0bY07eGA6i4/edit#gid=798220679

*The fourth algorithm included in the Bagel data simply represents the third algorithm with the first guess randomized. This random-version, although not used for Mastermind testing, represents the default version moving forward.*

*The fifth algorithm in the Bagel data and fourth in the MasterMind data reflects the update 1/16/20 update to prioritize valid configurations. This vastly reduced the average number of guesses for both games.*
