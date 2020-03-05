import nn
from baseBrain import BaseBrain


class nnBrain(BaseBrain):

    class NeuralNetwork:

        def __init__(self, nn_parameters=None, nn1=None, nn2=None):
            self.layers = []
            if nn_parameters:
                if nn1 is not None or nn2 is not None:
                    raise ValueError("can't have both nn_parameters and nn1, nn2")

                for layer in nn_parameters:
                    self.layers.append(layer[0](*layer[1]))
            else:
                raise NotImplementedError
       
        def forward(self, x):
            for layer in self.layers:
                x = layer.forward(x)
            return x


    def __init__(self, commands=None, command_limit=None, data=None):
        self.net = self.NeuralNetwork(*data) if data else None
        

    def make_a_move(self, sensor_data):
        pass
