import brain

class Agent:
    """
    A creature that will live in the artificial environment

    Attributes
    ----------
    pos : tuple (x, y)
        Position in the grid
    energy : int
        Energy of the creature when it is born
    brain : random, interpreter or neural network Brain
        Decision-making unit of the creature
    make_a_move : method
        brain.make_a_move to save typing
    """

    def __init__(self, pos, energy, energy_cap, radius, brain_type, brain_settings):
        """
        Parameters
        ----------
        pos : tuple (x, y)
            Position in the grid
        energy : int
            Energy of the creature when it is born
        brain_type : str
            Type of brain to be used
        brain_settings: tuple
            All the settings needed in brain init
        """
        self.pos = pos
        self.energy = energy
        self.energy_cap = energy_cap
        self.radius = radius
        if brain_type == 'random':
            self.brain = brain.RandomBrain(*brain_settings)
        elif brain_type == 'interpreter':
            self.brain = brain.InterpreterBrain(*brain_settings)
        else:
            raise NotImplementedError

        self.make_a_move = self.brain.make_a_move

def main():
    """Small testing case"""
    a = Agent((0, 0), 50, 255, 1, 'random', (10,))
    print(a)
    for i in range(10):
        print(a.make_a_move(None))

if __name__ == '__main__':
    main()
