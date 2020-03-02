import nn
from baseBrain import BaseBrain


class nnBrain(BaseBrain):

    class NeuralNetwork:

        def __init__(self, parameters=None, nn1=None, nn2=None):
            self.layers = []
            if parameters:
                for layer in parameters:
                    print(layer)
                    self.layers.append(layer[0](*layer[1]))


                self.d = parameters[0][0](*(parameters[0][1]))
                self.a = parameters[1][0](*(parameters[1][1]))
            else:
                raise NotImplementedError
       
        def forward(self, x):
            for layer in self.layers:
                x = layer.forward(x)
            return x


    def __init__(self, nn_parameters):
        self.net = self.NeuralNetwork(*nn_parameters)

    def make_a_move(self, sensor_data):
        pass
