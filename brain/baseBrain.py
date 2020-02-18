from abc import ABC, abstractmethod
class BaseBrain(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def make_a_move(self, sensor_data):
        raise NotImplementedError
