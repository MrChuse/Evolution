from baseBrain import BaseBrain
import logging

class InterpreterBrain(BaseBrain):

    class ModuloInteger:
        def __new__(cls, value, modulo):
            return object.__new__(cls)

        def __init__(self, value, modulo):
            self.value = value
            self.modulo = modulo

        def __add__(self, other):
            return (self.value + other) % self.modulo

        def __iadd__(self, other):
            new = self.__new__(type(self), self + other, self.modulo)
            new.__init__(self + other, self.modulo)
            return new

        def __str__(self):
            return str(self.value)

        def __index__(self):
            return self.value

        def __gt__(self, other):
            return self.value > other.value

    def __init__(self, data, commands, command_limit):
        self.data = data
        self.commands = commands
        self.command_limit = command_limit

        self.pointer = self.ModuloInteger(0, len(data))
        self.counter_limit = 0

    def make_a_move(self, sensor_data):
        while self.counter_limit < self.command_limit:
            #print(self.pointer,str(type(self.pointer)))
            current_command_id = self.data[self.pointer]
            if current_command_id >= len(self.commands):
                self.pointer += 1
                self.counter_limit += 1
                continue
            if self.commands[current_command_id][1] is True:
                from_data = self.pointer
                #print(from_data, 'from_data')
                self.pointer += (self.commands[current_command_id][0] + 1)
                #print(self.data[from_data : self.pointer], from_data, self.pointer)
                if from_data > self.pointer:
                    ret = self.data[from_data:] + self.data[:self.pointer]
                else:
                    ret = self.data[from_data : self.pointer]
                return ret

        return -1

def main():
    data = [0, 0, 0, 0, 0, 0, 0, 1]
    commands = [(0, True), (1, True), (2, False)]
    command_limit = 10
    brain = InterpreterBrain(data, commands, command_limit)
    for i in range(10):
        print(brain.make_a_move(None))

if __name__ == '__main__':
    main()
