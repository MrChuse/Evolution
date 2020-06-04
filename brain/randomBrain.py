import random
from brain.baseBrain import BaseBrain

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

    def __init__(self, commands, command_limit, data=None):
        self.data = data
        self.commands = commands
        self.command_limit = command_limit
        self.counter_limit = 0

    def make_a_move(self, sensor_data=None):
        a = int(random.random() * len(self.commands))
        while self.commands[a][1] is False and self.counter_limit < self.command_limit:
            a = int(random.random() * len(self.commands))
            self.counter_limit += 1
        if self.commands[a][1] is False:
            return -1
        return [a] + [int(random.random() * 64) for i in range(self.commands[a][0])]

    def mutate(self, rng, mutation_settings):
        pass
