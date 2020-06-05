from Agent import Agent
import random, sys

class CellType:
    """
    A class defines the basic cell configuration.

    Attributes
    ----------
    type_number : int, optional
        the number that specifies the type of cell (default is 0)
        0 - Base type
        (other types will be described later)
    food : int, optional
        the amount of food in the cell (default is 0)
        a number in range [0, 127]
    temperature : int, optional
        cell temperature (default is 0)
        a number in range [-64, 63]
    energy_value : int, optional
        the amount of energy
        that the agent receives eating 1 food (default is 1)
        a number in range [1, 15]
    """

    def __init__(self, type_number=0, food=0, temperature=0, energy_value=1):
        self.type_number = type_number
        self.food = food
        self.temperature = temperature
        self.energy_value = energy_value


class Cell:
    """
    A class that implements interaction with a cell.

    Attributes
    ----------
    cell_type : int, optional
        the number that specifies the type of cell (default is 0)
        0 - Base type
        (other types will be described later)
    agent : int(?), optional
        a pointer to the agent located in the cell (default is None)

    Methods
    -------
    is_food_here
        says whether food in in the cell (bool)
    get_food
        returns the amount of energy an agent will receive
        if there is no food returns 0
    get_amount_of_food
        returns the amount of food in the cell
    get_temperature
        returns cell temperature
    get_cell_type
        returns cell type
    """

    def __init__(self, cell_type=0, agent=None):
        self.cell_type = CellType(cell_type)
        self.agent = agent

    def is_food_here(self):
        return self.cell_type.food > 0

    def get_food(self):
        if not self.is_food_here:
            return 0

        self.cell_type.food -= 1
        return self.cell_type.energy_value

    def get_amount_of_food(self):
        return self.cell_type.food

    def get_temperature(self):
        return self.cell_type.temperature

    def get_cell_type(self):
        return self.cell_type.type_number

class Field:
    """
    A class that implements interaction with field.

    Attributes
    ----------
    width : int, optional
        field width (default is 5)
    height : int, optional
        field height (default is 5)
    photosyn_nrg : int, optional
        amount of energy which agent will get during photosynthesis
    ----------
    q : Queue()
        agents order
    agents : 2D array
        pointers to agents placed on field
    field : 2D array
        2D array of cells


    Methods
    -------
    spawn_agent (pos, energy, brain_type, brain_settings)
        creates an agent and spawns it on the field
    get_next_agent
        returns the next agent from the queue
    kill_agent (target_pos)
        kills agent and returns amount of his energy
    is_occupied (target_pos)
        says whether the cell is occupied (bool)
    make_a_move (agent_pos, step)
        returns new agent's position (tuple) if it's allowed
    photosyn (agent)
        add energy recieved during photosynthesis to the agent
    eat (agent, target_pos)
        if cell isn't occupied, agent will take 1 point of food
        otherwise agent will kill another agent and get his energy
    get_info (agent_pos, target_pos)
        agent will get information about target cell:
        is it occupied? is there any food?
        returns tuple
    give_birth_to (agent, target_pos, energy)
        spawn a child with a given energy
    do_nothing
        do nothing
    temperature_effect (agent):
        a method that reduces the energy of an agent
        based on the temperature of the cell on which it's located
    """

    def __init__(self, width=48, height=48, photosyn_nrg=8):
        self.width = width
        self.height = height
        self.photosyn_nrg = photosyn_nrg
        self.q = []

        self.agents = []
        self.field = []
        for i in range(width):
            self.agents.append([])
            self.field.append([])
            for j in range(height):
                c = Cell()
                c.cell_type.temperature = -int(j / height * 64) + 64
                self.field[i].append(c)
                self.agents[i].append(None)

        seed = random.randrange(sys.maxsize)
        self.rng = random.Random(seed)
        print("Seed is:", seed)

    def spawn_agent(self, pos, brain_settings, energy=50, energy_cap=255, radius=1, brain_type='interpreter'):
        self.agents[pos[0]][pos[1]] = Agent(pos, energy, energy_cap, radius, brain_type, brain_settings)
        self.q.append(pos)

    def kill_agent(self, target_pos):
        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        a = self.agents[target_pos[0]][target_pos[1]]
        self.agents[target_pos[0]][target_pos[1]] = None
        self.q.remove((target_pos[0], target_pos[1]))

        return a.energy

    def is_occupied(self, target_pos):
        return self.agents[target_pos[0]][target_pos[1]] is not None

    def make_a_move(self, agent, new_pos, index):
        if new_pos[0] < 0 or new_pos[0] >= self.width:
            return agent.pos

        if new_pos[1] < 0 or new_pos[1] >= self.height:
            return agent.pos

        if abs(agent.pos[0] - new_pos[0]) > agent.radius or abs(agent.pos[1] - new_pos[1]) > agent.radius:
            return agent.pos

        if self.is_occupied(new_pos):
            return agent.pos

        agent.energy -= 8 * max(abs(agent.pos[0] - new_pos[0]), abs(agent.pos[1] - new_pos[1]))
        self.agents[agent.pos[0]][agent.pos[1]] = None
        agent.pos = new_pos
        self.agents[new_pos[0]][new_pos[1]] = agent
        self.q[index] = new_pos

        return agent.pos

    def photosyn(self, agent):
        agent.energy = min(agent.energy_cap, (agent.energy + self.photosyn_nrg))

    def eat(self, agent, target_pos, index):
        if agent.pos == target_pos:
            return

        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if abs(agent.pos[0] - target_pos[0]) > agent.radius or abs(agent.pos[1] - target_pos[1]) > agent.radius:
            return

        if not self.is_occupied(target_pos):
            agent.energy = min(agent.energy + self.field[target_pos[0]][target_pos[1]].get_food(), agent.energy_cap)
        else:
            received_energy = self.kill_agent(target_pos)
            agent.energy = min(agent.energy_cap, agent.energy + received_energy)
            self.agents[target_pos[0]][target_pos[1]] = None

    def get_info(self, agent, target_pos):
        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if abs(agent.pos[0] - target_pos[0]) > agent.radius or abs(agent.pos[1] - target_pos[1]) > agent.radius:
            return

        is_occupied = self.is_occupied(target_pos)
        is_food_here = self.field[target_pos[0]][target_pos[1]].is_food_here()
        amount_of_food = self.field[target_pos[0]][target_pos[1]].get_amount_of_food()
        temperature = self.field[target_pos[0]][target_pos[1]].get_temperature()

        return is_occupied, is_food_here, amount_of_food, temperature

    def get_sensor_data(self, agent):
        sensor_data = []
        for di in range(-agent.radius, agent.radius + 1):
            for dj in range(-agent.radius, agent.radius + 1):
                if (agent.pos[0] + di) < 0 or (agent.pos[0] + di) >= self.width:
                    continue
                if (agent.pos[1] + dj) < 0 or (agent.pos[1] + dj) >= self.height:
                    continue
                sensor_data.append(self.get_info(agent, (agent.pos[0] + di, agent.pos[1] + dj)))

    def give_birth_to(self, agent, target_pos, energy, brain_settings, mutation_settings):
        if agent.energy < energy:
            return

        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if self.is_occupied(target_pos):
            return

        self.spawn_agent(target_pos, brain_settings, energy)
        agent.energy -= energy

        self.agents[target_pos[0]][target_pos[1]].mutate(self.rng, mutation_settings)

    def do_nothing(self):
        pass

    def temperature_effect(self, agent):
        t = self.field[agent.pos[0]][agent.pos[1]].get_temperature()
        agent.energy -= (abs(t) // 8 + 1)

    def brain_size_effect(self, agent):
        brain_size = agent.get_brain_size()
        if brain_size <= 64:
            agent.energy -= round(0.5 * brain_size ** 0.5)
        else:
            agent.energy -= round((brain_size - 64) ** 2 + 4)

    def share_energy(self, agent, target_pos, amount_of_energy):
        if agent.energy < amount_of_energy:
            return

        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if self.agents[target_pos[0]][target_pos[1]] is None:
            return

        if abs(agent.pos[0] - target_pos[0]) > agent.radius or abs(agent.pos[1] - target_pos[1]) > agent.radius:
            return

        agent.energy -= amount_of_energy
        target_agent = self.agents[target_pos[0]][target_pos[1]]
        target_agent.energy = min(255, target_agent.energy + amount_of_energy)
