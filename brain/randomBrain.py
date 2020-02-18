import random
from baseBrain import BaseBrain

class RandomBrain(BaseBrain):

    def __init__(self, number_of_moves):
        self.number_of_moves = number_of_moves

    def make_a_move(self, sensor_data):
        return int(random.random() * self.number_of_moves)
