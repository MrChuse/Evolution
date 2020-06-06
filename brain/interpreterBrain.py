from brain.baseBrain import BaseBrain
import logging

class InterpreterBrain(BaseBrain):
    """
    This class implements a decision-making machine with a turing-complete language

    Sub Classes
    -----------
    ModuloInteger
        A class to perform modulo arithmetics

    Attributes
    ----------
    data : list of ints
        The program to be interpreted (should not be changed)
    commands : list of tuples (create a Command class?)
        All possible actions of the environment
    command_limit : int
        Limits the number of commands executed before final action
    pointer : ModuloInteger
        Pointer of the current command
    counter_limit : int
        Counter of not final commands executed

    Methods
    -------
    make_a_move(self, sensor_data):
        calculates the next action and moves pointer further
    mutate(self, prob, number_of_bytes=1):
        changes number_of_bytes commands in the data with probability prob
    """

    class ModuloInteger:
        def __new__(cls, value, modulo):
            return object.__new__(cls)

        def __init__(self, value, modulo):
            self.value = value
            self.modulo = modulo

        def __add__(self, other):
            new = self.__new__(type(self), (self.value + other) % self.modulo, self.modulo)
            new.__init__((self.value + other) % self.modulo, self.modulo)
            return new

        def __iadd__(self, other):
            return self + other

        def __str__(self):
            return str(self.value)

        def __index__(self):
            #print(type(self.value))
            return self.value

        def __gt__(self, other):
            return self.value > other.value

        def __ge__(self, other):
            return self.value >= other.value

    def __init__(self, commands, command_limit,  data):
        """
        Parameters
        ----------
        data : list of ints
            The program to be interpreted (should not be changed)
        commands : list of tuples (create a Command class?)
            All possible actions of the environment
        counter_limit : int
            Counter of not final commands executed
        """
        self.data = data
        self.commands = commands
        self.command_limit = command_limit

        self.pointer = self.ModuloInteger(0, len(data))
        self.counter_limit = 0

    def make_a_move(self, sensor_data=None):
        """
        Main method for the interpreter

        Parameters
        ----------
        sensor_data : ???
            All the data provided by the environment

        Summary of the code:
            READ the command from data[pointer]
            IF it is final command THEN return that action and its arguments
            ELSE execute that command (it shouldn't interact with the world,
                 only with visible data or the pointer)
            move the pointer to the next command

        TODO: conditional and unconditional jumps, vision of the data
        """

        self.counter_limit = 0
        #execute commands until the limit is reached
        while self.counter_limit < self.command_limit:
            current_command_id = self.data[self.pointer]
            if current_command_id >= len(self.commands):
                self.pointer += 1      #if command is invalid, move the pointer,
                self.counter_limit += 1  #update the counter, proceed to the next command
                continue

            left_data = self.pointer #calculate
            right_data = self.pointer + self.commands[current_command_id][0] + 1

            if left_data >= right_data: #check for the overlap
                command_and_arguments = self.data[left_data:] + self.data[:right_data]
            else:
                command_and_arguments = self.data[left_data : right_data]

            if self.commands[current_command_id][1] is True: #if the command is final
                self.pointer = right_data
                return command_and_arguments #return action and its arguments
            else:
                try:
                    #print(type(self.pointer),self.pointer.value, 'in the else, try')
                    self.pointer += self.commands[current_command_id][2](sensor_data, command_and_arguments)
                    #print(type(self.pointer),self.pointer.value, 'in the else, after try')
                except Exception:
                    #print(type(self.pointer),self.pointer.value, 'in the except')
                    self.pointer += 1
                    #print(type(self.pointer),self.pointer.value, 'in the except 2')
                    continue
                finally:
                    self.counter_limit += 1
        return -1 #return -1 if no action was chosen

    def mutate(self, rng, mutation_settings):
        for i in range(mutation_settings.number_of_brain_changes):
            if rng.random() < mutation_settings.change_gene_probability:
                gene = int(rng.random() * len(self.data))
                self.data[gene] = int(rng.random() * mutation_settings.gene_max)
        if rng.random() < mutation_settings.change_brain_size_probability:
            dsize = int(rng.random() * (2 * mutation_settings.max_brain_size_change + 1)) - mutation_settings.max_brain_size_change
            if dsize == 0:
                return
            if dsize > 0:
                for i in range(dsize):
                    self.data.append(int(rng.random() * mutation_settings.gene_max))
            else:
                for i in range(-dsize):
                    self.data.pop(int(rng.random() * len(self.data)))
            self.pointer = self.ModuloInteger(0, len(self.data))

    def check_ally(self, other, param):
        d = 0
        for index in range(min(len(self.data), len(other.data))):
            if self.data[index] != self.data[index]:
                d += 1
        return d <= param

    def get_brain_size(self):
        return len(self.data)


def main():
    data = [3, 3, 4, 1, 0, 0, 0, 1]
    photosynthesis = (0, True) # id = 0
    move = (1, True) # id = 1
    unconditional_jump = (1, False, lambda x, y: y[1])
    check_field = (3, False, lambda x, y: y[2] if x[y[1]]%2 == 0 else y[3])
    commands = [photosynthesis, move, unconditional_jump, check_field]
    command_limit = 10
    brain = InterpreterBrain(commands, command_limit, data)
    for i in range(10):
        #print(i, 'th move')
        print(brain.make_a_move([0, 1, 0, 1, 0, 1, 0, 1, 0]), 'picked_move')

if __name__ == '__main__':
    main()
