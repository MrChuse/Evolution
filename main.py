import core
from Agent import Agent

def new_id():
    id = -1
    while True:
        yield id
        id -= 1

def draw(field):
    for row in field.field:
        for cell in row:
            if cell.agent is None:
                print(cell.cell_type, end='')
            else:
                print(cell.agent.id)

total_cycles = 100

width, height = 10, 10

field = core.Field(width, height)
agents = [Agent(new_id(), (width//2, height//2), 100, 'random', field.get_commands())]
field.add_agents(agents)



for cycle in range(total_cycles):
    for agent in agents:
        field.do_action(agent, agent.make_a_move(field.get_sensor_data(agent)))
    draw(field)
