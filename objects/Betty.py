import math
import random

# Probably a mixin to the Player class

"""

Actions determine whether AI decides to bet. Reactions determine whether to follow player's bet.

"""


def action_linear(Comp):
    """
    AI will bet if a uniform random number is smaller than the log-linear score of the AI's hand. Better hand, larger
    log-linear score and more likely to bet.
    """

    Comp.update_score()
    log_score = math.log10(Comp.hand.score)
    if random.uniform(0, 2.5) < log_score:
        return True

    return False
