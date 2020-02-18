from baseBrain import BaseBrain
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

    def make_a_move(self, sensor_data):
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

        #execute commands until the limit is reached
        while self.counter_limit < self.command_limit:
            current_command_id = self.data[self.pointer]
            if current_command_id >= len(self.commands):
                self.pointer += 1      #if command is invalid, move the pointer,
                self.counter_limit += 1  #update the counter, proceed to the next command
                continue
            if self.commands[current_command_id][1] is True: #if the command is final
                from_data = self.pointer
                self.pointer += (self.commands[current_command_id][0] + 1) #move the pointer
                if from_data > self.pointer: #check for the overlap
                    ret = self.data[from_data:] + self.data[:self.pointer]
                else:
                    ret = self.data[from_data : self.pointer]
                return ret #return action and its arguments
            else: #TODO: jumps, vision
                pass
        return -1 #return -1 if no action was chosen

def main():
    data = [0, 0, 0, 0, 0, 0, 0, 1]
    commands = [(0, True), (1, True), (2, False)]
    command_limit = 10
    brain = InterpreterBrain(data, commands, command_limit)
    for i in range(10):
        print(brain.make_a_move(None))

if __name__ == '__main__':
    main()
