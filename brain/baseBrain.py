from abc import ABC, abstractmethod

class BaseBrain(ABC):
    """
    Base class for all brains to inherit

    Methods
    -------
    make_a_move(self, sensor_data):
        The main method to calculate the next move

    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def make_a_move(self, sensor_data):
        raise NotImplementedError
