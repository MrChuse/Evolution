import nn
from baseBrain import BaseBrain


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


class nnBrainUniversal(BaseBrain):

    def __init__(self, commands=None, command_limit=None, data=None):
        self.net = NeuralNetwork(*data) if data else None
        self.commands = commands
        self.out_parameters = 0
        self.reference = []
        for index, command in enumerate(commands):
            if command[1] is True:
                self.out_parameters = max(self.out_parameters, command[0])
                self.reference.append(index)
        
    def make_a_move_with_nn(self, sensor_data):
        data = extract_data(sensor_data)
        ret = map(int, data)
        ret[0] = self.reference[ret[0]]
        return ret[:self.out_parameters + 1]

    def make_a_move(self, sensor_data):
        if self.net is None:
            self.net = NeuralNetwork(nn_parameters_from_sensor_data(sensor_data))
        self.make_a_move = self.make_a_move_with_nn
        return self.make_a_move_with_nn(sensor_data)
