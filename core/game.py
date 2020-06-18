from core.field import Field
from core.baseCommands import base_commands
from core.statistics import Statistics

import copy
import time
import pickle
import os
from collections import namedtuple


def from_position_to_dx_dy(position, radius):
    """
     9 13 17 21 10 - spiral
    24  1  5  2 14
    20  8  0  6 18
    16  4  7  3 22
    12 23 19 15 11
    position: int
        the position on the spiral
    radius: positive int
        max radius of the spiral
    returns dx, dy tuple - position relative to 0
    """
    # reduce position to spiral size
    position %= (2 * radius + 1) ** 2

    if position == 0:
        return 0, 0
    cycle = 0
    for i in range(1, radius + 1):
        if position >= (2 * i + 1) ** 2:
            continue
        cycle = i
        break
    if cycle == 0:
        print(position, radius, 'pos, radius')
        raise ValueError('cycle is 0')

    d = (position - (2 * cycle - 1) ** 2) // 4
    if position % 4 == 1:
        return -cycle + d, -cycle  # up
    elif position % 4 == 2:
        return cycle, -cycle + d  # right
    elif position % 4 == 3:
        return cycle - d, cycle  # down
    else:
        return -cycle, cycle - d  # left


class Game:
    def __init__(self, empty=None):
        # directories stuff
        try:
            os.mkdir('./worlds')
        except FileExistsError:
            pass
        try:
            os.mkdir('./agents')
        except FileExistsError:
            pass

        # game stuff
        if empty:
            self.field = None
        else:
            self.field = Field(seed=4952008353301190740)
        self.stats = Statistics()
        self.tick = 0
        self.move_period = 50
        self.MutationSettings = namedtuple('MutationSettings',
                                           ['change_radius_probability',
                                            'change_energy_cap_probability',
                                            'mutate_brain_probability',
                                            'number_of_brain_changes',
                                            'change_gene_probability',
                                            'gene_max',
                                            'change_brain_size_probability',
                                            'max_brain_size_change'],
                                           defaults=(None,) * 5)

        data = [0] * 5 + [4, 5, 32] + [0] * 5 + [4, 6, 32] + [0] * 5 + [4, 7, 32] + [0] * 5 + [4, 8, 32]
        command_limit = 10
        brain_settings = (base_commands, command_limit, data)
        self.base_brain_settings = brain_settings

        self.base_mutation_settings = self.MutationSettings(0.1, 0.1, 0.1, number_of_brain_changes=3,
                                                            change_gene_probability=0.2, gene_max=64,
                                                            change_brain_size_probability=0.2,
                                                            max_brain_size_change=2)
        
        self.field.spawn_agent((self.field.width // 2, self.field.height // 2),
                               self.base_brain_settings, brain_type='interpreter')

    def update(self):
        # print(len(self.field.q))
        self.field.add_minerals()
        total_bots = 0
        bots_energy = 0
        sum_brain_size = 0
        max_brain_size = 0
        for index, pos in enumerate(self.field.q):
            agent = self.field.field[pos[0]][pos[1]].agent

            if agent is None:
                continue

            if not agent.alive:
                if not self.field.field[pos[0]][pos[1]].is_meat_here():
                    self.field.q.remove(pos)
                    self.field.field[pos[0]][pos[1]].agent = None
                continue
              
            # stats
            total_bots += 1
            bots_energy += agent.energy
            bots_energy += agent.energy
            brain_size = agent.get_brain_size()
            sum_brain_size += brain_size
            if brain_size > max_brain_size:
                max_brain_size = brain_size

            commands_and_arguments = agent.make_a_move(self.field.get_sensor_data(agent))
            if commands_and_arguments[0] == -1:
                continue
            if commands_and_arguments[0] == 0:  # id = 0 == photosyn
                self.field.photosyn(agent)
            elif commands_and_arguments[0] == 1:  # id = 1 == make_a_move
                dx, dy = from_position_to_dx_dy(commands_and_arguments[1], agent.radius)
                self.field.make_a_move(agent, (agent.pos[0] + dx, agent.pos[1] + dy), index)
            elif commands_and_arguments[0] == 2:  # id = 2 == eat
                dx, dy = from_position_to_dx_dy(commands_and_arguments[1], agent.radius)
                self.field.eat(agent, (agent.pos[0] + dx, agent.pos[1] + dy), index)
            elif commands_and_arguments[0] == 3:  # id = 3 == eat_mineral
                dx, dy = from_position_to_dx_dy(commands_and_arguments[1], agent.radius)
                self.field.eat_mineral(agent, (agent.pos[0] + dx, agent.pos[1] + dy))
            elif commands_and_arguments[0] == 4:  # id = 4 == give_birth_to
                dx, dy = from_position_to_dx_dy(commands_and_arguments[1], agent.radius)
                child_energy = agent.energy * commands_and_arguments[2] // 64 + 1
                brain_settings = (agent.brain.commands, agent.brain.command_limit, copy.deepcopy(agent.brain.data))
                self.field.give_birth_to(agent, (agent.pos[0] + dx, agent.pos[1] + dy),
                                         child_energy, brain_settings, self.base_mutation_settings)
            elif commands_and_arguments[0] == 5:  # id = 5 == share_energy
                dx, dy = from_position_to_dx_dy(commands_and_arguments[1], agent.radius)
                amount_of_energy = agent.energy * commands_and_arguments[2] // 64 + 1
                self.field.share_energy(agent, (agent.pos[0] + dx, agent.pos[1] + dy), amount_of_energy)
            else:
                self.field.do_nothing()

            self.field.temperature_effect(agent)
            self.field.brain_size_effect(agent)
            if agent.energy < 0 and self.field.field[agent.pos[0]][agent.pos[1]].agent:
                self.field.kill_agent(agent.pos)
                self.field.field[agent.pos[0]][agent.pos[1]].add_meat(2)

            if agent.energy > agent.energy_cap:
                brain_settings = (agent.brain.commands, agent.brain.command_limit, copy.deepcopy(agent.brain.data))
                self.field.give_birth_random(agent, brain_settings, self.base_mutation_settings)

        if total_bots > 0:
            avg_bot_energy = (bots_energy / total_bots)
            avg_brain_size = (sum_brain_size / total_bots)
        else:
            avg_bot_energy = 0
            avg_brain_size = 0
        env_energy = 0
        # if total_bots > 2304:
            # print(total_bots, len(self.field.q))
        self.stats.add_tick(num_agents=total_bots,
                            bots_energy=bots_energy,
                            avg_bot_energy=avg_bot_energy,
                            env_energy=env_energy, 
                            total_energy=bots_energy + env_energy,
                            avg_brain_len=avg_brain_size,
                            max_brain_len=max_brain_size)
        self.tick += 1
        if self.tick % self.move_period == 0:
            self.field.move_field()

    def save_game_to_file(self, name='game1'):
        proper_path = './worlds/' + name + '.wld'
        with open(proper_path, 'wb') as fout:
            pickle.dump((self.field, self.stats), fout)

    def load_game_from_file(self, name='game1'):
        proper_path = './worlds/' + name + '.wld'
        with open(proper_path, 'rb') as fin:
            self.field, self.stats = pickle.load(fin)

    @staticmethod
    def save_agent_to_file(agent, name='agent1'):
        proper_path = './agents/' + agent.name[:3] + '_rad' + str(agent.radius) + '_nrg' + str(agent.energy_cap) + '_' + name + '.agn'
        with open(proper_path, 'wb') as fout:
            pickle.dump(agent, fout)

    @staticmethod
    def load_agent_from_file(name='agent1'):
        proper_path = './agents/' + name + '.agn'
        with open(proper_path, 'rb') as fin:
            return pickle.load(fin)

    @staticmethod
    def get_all_world_names():
        return [i[:-4] for i in os.listdir(path="./worlds")]

    @staticmethod
    def get_all_agent_names():
        return [i[:-4] for i in os.listdir(path="./agents")]


def print_map(g):
    for row in g.field.agents:
        for element in row:
            print(f'%-12s' % str(element), end=' ')
        print()
    print()


def print_energy_map(g):
    for row in g.field.agents:
        for element in row:
            if element is None:
                print(f'%-4d' % 0, end=' ')
            elif not element.alive:
                print(f'%-4d' % -1, end=' ')
            else:
                print(f'%-4d' % element.energy, end=' ')
        print()
    print()


def main():
    g = Game()
    # g.field.spawn_agent((0, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    # g.field.spawn_agent((g.field.width - 1, g.field.height - 1), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    # g.field.spawn_agent((0, g.field.height - 1), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    # g.field.spawn_agent((g.field.width - 1, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')

    while True:
        # print_energy_map(g)
        g.update()
        # time.sleep(0.25)


if __name__ == '__main__':
    main()
