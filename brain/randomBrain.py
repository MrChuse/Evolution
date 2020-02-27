import random
from baseBrain import BaseBrain

class RandomBrain(BaseBrain):
    """
    The simplest (and probably the dumbest) brain possible

    Attributes
    ----------
    number_of_moves : int
        The number of possible actions an environment has

    Methods
    -------
    make_a_move(self, sensor_data):
        returns a random number from 0 to number_of_moves
    """

    def __init__(self, number_of_moves):
        self.number_of_moves = number_of_moves

    def make_a_move(self, sensor_data):
        return int(random.random() * self.number_of_moves)
