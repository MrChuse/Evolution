from core.field import Field
import time


class Game:
    def __init__(self):
        self.field = Field()

        data = [0] * 32
        photosynthesis = (0, True)  # id = 0
        move = (2, True)  # id = 1
        eat = (2, True)  # id = 2
        unconditional_jump = (1, False, lambda x, y: y[1])
        commands = [photosynthesis, move, eat, unconditional_jump]
        command_limit = 10
        brain_settings = (commands, command_limit, data)
        self.field.spawn_agent((self.field.width // 2, self.field.height // 2), brain_settings)

    def update(self):
        for index, pos in enumerate(self.field.q):
            agent = self.field.agents[pos[0]][pos[1]]
            if agent is None:
                continue

            commands_and_arguments = agent.make_a_move(self.field.get_sensor_data(agent))
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
            else:
                self.field.do_nothing()
            self.field.temperature_effect(agent)


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
    g.field.spawn_agent((0, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    g.field.spawn_agent((4, 4), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    g.field.spawn_agent((0, 4), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
    g.field.spawn_agent((4, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')

    while True:
        print_map(g)
        g.update()
        time.sleep(0.5)


if __name__ == '__main__':
    main()
