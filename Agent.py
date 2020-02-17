import brain

class Agent:

    def __init__(self, pos, energy, brain_type, brain_settings):
        self.pos = pos
        self.energy = energy
        if brain_type == 'random':
            self.brain = brain.RandomBrain(*brain_settings)
        else:
            raise NotImplementedError

        self.make_a_move = self.brain.make_a_move

def main():
    a = Agent((0,0), 50, 'random', (10,))
    print(a)
    for i in range(10):
        print(a.make_a_move(None))

if __name__ == '__main__':
    main()
