from core.field import Field
from core.baseCommands import base_commands
from core.statistics import Statistics

import copy
import time
import pickle
import os
from collections import namedtuple


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
            self.field = Field()
        self.stats = Statistics()
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

        data = [0] * 4 + [3, 1, 0, 32] + [0] * 4 + [3, 0, 1, 32] + [0] * 4 + [3, 1, 2, 32] + [0] * 4 + [3, 2, 1, 32]
        command_limit = 10
        brain_settings = (base_commands, command_limit, data)
        self.base_brain_settings = brain_settings

        self.base_mutation_settings = self.MutationSettings(0.1, 0.1, 0.1, number_of_brain_changes=3,
                                                            change_gene_probability=0.2, gene_max=64,
                                                            change_brain_size_probability=0.2,
                                                            max_brain_size_change=2)
        
        self.field.spawn_agent((self.field.width // 2, self.field.height // 2),
                               self.base_brain_settings, brain_type='interpreter')

        # self.max_energy_cap = -1

    def update(self):
        self.field.add_minerals()
        total_bots = 0
        bots_energy = 0
        sum_brain_size = 0
        max_brain_size = 0
        for index, pos in enumerate(self.field.q):
            # agent = self.field.agents[pos[0]][pos[1]]
            agent = self.field.field[pos[0]][pos[1]].agent

            if agent is None:
                continue

            if not agent.alive:
                if not self.field.field[pos[0]][pos[1]].is_meat_here():
                    self.field.q.remove(pos)
                    # self.field.agents[pos[0]][pos[1]] = None
                    self.field.field[pos[0]][pos[1]].agent = None
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
            if commands_and_arguments[0] == -1:
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
