import brain
from collections import defaultdict

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
        self.name = brain_type
        self.alive = True
        if brain_type == 'random':
            self.brain = brain.RandomBrain(*brain_settings)
        elif brain_type == 'interpreter':
            self.brain = brain.InterpreterBrain(*brain_settings)
        else:
            raise NotImplementedError
        self.eats = defaultdict(int)
        self.max_eats = 100
        self.make_a_move = self.brain.make_a_move
        self.get_brain_size = self.brain.get_brain_size

    def __str__(self):
        return self.name

    def clamp_eats(self):
        s = 0
        for value in self.eats.values():
            s += value
        if s > self.max_eats:
            for key in self.eats.keys():
                self.eats[key] = max(0, self.eats[key] - 1)

    def mutate(self, rng, mutation_settings):
        if rng.random() > mutation_settings.change_radius_probability:
            dr = rng.random()
            if dr > 0.5:
                self.radius += 1
            else:
                self.radius = max(1, self.radius - 1)
        if rng.random() > mutation_settings.change_energy_cap_probability:
            dcap = int(rng.random() * 33 - 16)
            self.energy_cap = max(16, self.energy_cap + dcap)
        if rng.random() > mutation_settings.mutate_brain_probability:
            self.brain.mutate(rng, mutation_settings)



def main():
    """Small testing case"""
    a = Agent((0, 0), 50, 255, 1, 'random', (10,))
    print(a)
    for i in range(10):
        print(a.make_a_move(None))

if __name__ == '__main__':
    main()
