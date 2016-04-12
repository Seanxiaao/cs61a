"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    L = [x for x in range(10)]
    i ,fff = 0 , False
    while  i < num_rolls:
         L[i] = dice()
         if L[i] == 1:
            fff = True
         i = i + 1
    p = sum(L[i] for i in range(num_rolls))
    if fff:
        return 0
    else:
        return p
    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    def is_prime(n):
        k = n - 2
        if n == 2:
           return True
        while n % k != 0:
            k = k - 1
        return k == 1

    def next_prime(n):
        m = n + 1
        while not is_prime(m):
            m = m + 1
        return m

    a, b, c = 0, 0, 0

    if num_rolls == 0:
        a= int(opponent_score/100)
        b= int(opponent_score/10)
        c= int(opponent_score-100*a-10*b)
        q= max(a,b,c)+1
    else: q = roll_dice(num_rolls, dice)
    if is_prime(q):
         return next_prime(q)
    else:
         return q
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0:
           dice = four_sided
           return dice
    else:
           dice = six_sided
           return dice
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    if score0 >= 100:
        score0 = score0 - 100
    if score1 >= 100:
        score1 = score1 - 100
    if int(score1/10) == score0-int(score0/10)*10 and int(score0/10) == score1 - int(score1/10)*10:
        return True
    else: return False
    # END Question 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    p = 0
    while score0 < goal and score1 < goal:
        if player == 0:
            num_rolls = strategy0(score0,score1)
            k = take_turn(num_rolls,score1,dice=select_dice(score0,score1))
            if k == 0:
                score1 = score1 + num_rolls
            else:
                score0 = score0 + k
            if is_swap(score0,score1):
                p = score0
                score0 = score1
                score1 = p
        if player == 1:
                num_rolls = strategy1(score1,score0)
                m = take_turn(num_rolls,score0,dice=select_dice(score0,score1))
                if m == 0:
                    score0 = score0 + num_rolls
                else:
                    score1 = score1 + m
                if is_swap(score0,score1):
                    p = score0
                    score0 = score1
                    score1 = p
        player = other(player)
    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def roll_dice(*args):
        i,result = 0,0
        while i < num_samples:
             result = result+fn(*args)
             i = i + 1
        result = result/num_samples
        return result
    return roll_dice
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    Q =[x for x in range(10)]
    P =[10 for x in range(10)]
    i = 0
    for i in range(10):
       Q[i] = make_averaged(roll_dice,num_samples)(i+1,dice)
    for i in range(10):
        if Q[i] == max(Q):
            P[i] = i + 1
    return min(P)

    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:
        print('always_roll(0) win rate', average_win_rate(always_roll(0)))

    if True:
        print('final_strategy win rate', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    "*** REPLACE THIS LINE ***"


    a= int(opponent_score/100)
    b= int(opponent_score/10)
    c= int(opponent_score-100*a-10*b)
    q= max(a,b,c)+1

    if is_prime(q):
        q = next_prime(q)

    if q >= margin:
        return 0
    else:
        return num_rolls
    # END Question 8
def is_prime(n):
    k = n - 2
    if n == 2:
       return True
    while n % k != 0:
        k = k - 1
    return k == 1

def next_prime(n):
    m = n + 1
    while not is_prime(m):
        m = m + 1
    return m


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    "*** REPLACE THIS LINE ***"

    a= int(opponent_score/100)
    b= int(opponent_score/10)
    c= int(opponent_score-100*a-10*b)
    q= max(a,b,c)+1

    if is_prime(q):
        q = next_prime(q)

    if (score + q) < opponent_score and int(opponent_score/10) == (score + q)-int((score + q)/10)*10 and int((score + q)/10) == opponent_score - int(opponent_score/10)*10:
        return 0
    else:
        return num_rolls# Replace this statement
    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    combine the bacon_strategy and swap_strategy and try to gives the opponent
    4 numbered dice
    """
    # BEGIN Question 10
    "*** REPLACE THIS LINE ***"
    a= int(opponent_score/100)
    b= int(opponent_score/10)
    c= int(opponent_score-100*a-10*b)
    q= max(a,b,c)+1

    if is_prime(q):
        q = next_prime(q)

    if is_swap(score + q ,opponent_score) and score + q < opponent_score:
        return 0
    elif q >= 6 or (score + q + opponent_score) % 7 == 0:
        return 0
    else:
        return 4# Replace this statement
    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
