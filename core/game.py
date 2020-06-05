from core.field import Field
from core.statsistics import Statistics
from core.mutationSettings import MutationSettings

import copy, time


class Game:
    def __init__(self):
        self.field = Field()
        self.stats = Statistics()

        data = [0] * 12 + [3, 1, 0, 32] + [0] * 12 + [3, 0, 1, 32] + [0] * 12 + [3, 1, 2, 32] + [0] * 12 + [3, 2, 1, 32]
        photosynthesis = (0, True)  # id = 0
        move = (2, True)  # id = 1
        eat = (2, True)  # id = 2
        give_birth_to = (3, True)  # id = 3
        share_energy = (3, True)  # id = 4
        unconditional_jump = (1, False, lambda x, y: y[1])
        commands = [photosynthesis, move, eat, give_birth_to, share_energy, unconditional_jump]
        command_limit = 10
        brain_settings = (commands, command_limit, data)
        self.base_brain_settings = brain_settings
        self.base_mutation_settings = MutationSettings(0.1, 0.1, 0.1, number_of_brain_changes=3,
                                                       change_gene_probability=0.2, gene_max=64)
        self.field.spawn_agent((self.field.width // 2, self.field.height - 1),
                               self.base_brain_settings, brain_type='interpreter')

        # self.max_energy_cap = -1

    def update(self):
        total_bots = 0
        bots_energy = 0
        sum_brain_size = 0
        max_brain_size = -1

        for index, pos in enumerate(self.field.q):
            agent = self.field.agents[pos[0]][pos[1]]
            if agent is None:
                continue


            # stats
            total_bots += 1
            bots_energy += agent.energy
            brain_size = agent.get_brain_size()
            sum_brain_size += brain_size
            if brain_size > max_brain_size:
                max_brain_size = brain_size

            # if agent.energy_cap > self.max_energy_cap:
            #     self.max_energy_cap = agent.energy_cap

            commands_and_arguments = agent.make_a_move(self.field.get_sensor_data(agent))
            if commands_and_arguments == -1:
                continue
            if commands_and_arguments[0] == 0:  # id = 0 == photosyn
                self.field.photosyn(agent)
            elif commands_and_arguments[0] == 1:  # id = 1 == make_a_move
                dx = commands_and_arguments[1] % (2 * agent.radius + 1) - agent.radius
                dy = commands_and_arguments[2] % (2 * agent.radius + 1) - agent.radius
                self.field.make_a_move(agent, (agent.pos[0] + dx, agent.pos[1] + dy), index)
            elif commands_and_arguments[0] == 2:  # id = 2 == eat
                dx = commands_and_arguments[1] % (2 * agent.radius + 1) - agent.radius
                dy = commands_and_arguments[2] % (2 * agent.radius + 1) - agent.radius
                self.field.eat(agent, (agent.pos[0] + dx, agent.pos[1] + dy), index)
            elif commands_and_arguments[0] == 3:  # id = 3 == give_birth_to
                dx = commands_and_arguments[1] % (2 * agent.radius + 1) - agent.radius
                dy = commands_and_arguments[2] % (2 * agent.radius + 1) - agent.radius
                child_energy = agent.energy * commands_and_arguments[3] // 64 + 1
                brain_settings = (agent.brain.commands, agent.brain.command_limit, copy.deepcopy(agent.brain.data))
                self.field.give_birth_to(agent, (agent.pos[0] + dx, agent.pos[1] + dy),
                                         child_energy, brain_settings, self.base_mutation_settings)
            elif commands_and_arguments[0] == 4:  # id = 4 == share_energy
                dx = commands_and_arguments[1] % (2 * agent.radius + 1) - agent.radius
                dy = commands_and_arguments[2] % (2 * agent.radius + 1) - agent.radius
                amount_of_energy = agent.energy * commands_and_arguments[3] // 64 + 1
                self.field.share_energy(agent, (agent.pos[0] + dx, agent.pos[1] + dy), amount_of_energy)
            else:
                self.field.do_nothing()

            self.field.temperature_effect(agent)
            self.field.brain_size_effect(agent)
            if agent.energy < 0:
                self.field.kill_agent(agent.pos)

        avg_brain_size = sum_brain_size / total_bots
        self.stats.add_tick(total_bots, bots_energy, None, avg_brain_size, max_brain_size)




def print_map(g):
    for row in g.field.agents:
        for element in row:
            print(f'%-12s' % str(element), end=' ')
        print()
    print()


def print_energy_map(g):
    for row in g.field.agents:
        for element in row:
            if element is not None:
                print(f'%-4d' % element.energy, end=' ')
            else:
                print(f'%-4d' % 0, end=' ')
        print()
    print()


def main():
    g = Game()
    # g.field.spawn_agent((0, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    # g.field.spawn_agent((g.field.width - 1, g.field.height - 1), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    # g.field.spawn_agent((0, g.field.height - 1), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    # g.field.spawn_agent((g.field.width - 1, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')

    while True:
        print_energy_map(g)
        g.update()
        time.sleep(0.5)


if __name__ == '__main__':
    main()
