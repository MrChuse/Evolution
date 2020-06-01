from ..Agent import Agent
from queue import Queue

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
        returns the amount of food is in the cell
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
        field width (default is 1000)
    height : int, optional
        field height (default is 1000)
    raduis : int, optional
        the radius within which the agent can move, eat
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
        creates agent and spawn it on field
    get_next_agent
        returns the next agent from the queue
    kill_agent (target_pos)
        kills agent and returns amount of his energy
    is_occupied (target_pos)
        says whether the cell is occupied (bool)
    make_a_move (agent_pos, step)
        returns new agent's position (tuple) if it's allowed
    photosyn (agent)
        add energy getting during photosynthesis to the agent
    eat (agent, target_pos)
        if cell isn't occupied, agent will take 1 point of food
        otherwise agent will kill another agent and get his energy
    get_info (agent_pos, target_pos)
        agent will get information about target cell:
        is it occupied? is there any food?
        returns tuple
    """

    def __init__(self, width=1000, height=1000, radius=1, photosyn_nrg=8):
        self.width = width
        self.height = height
        self.radius = radius
        self.photosyn_nrg = photosyn_nrg
        self.q = Queue()
        self.agents = []
        self.field = []
        for i in range(width):
            for j in range(height):
                self.field[i][j] = Cell()
                self.agents[i][j] = None

    def spawn_agent(self, pos, energy, brain_type, brain_settings):
        self.agents[pos[0]][pos[1]] = Agent(pos, energy, brain_type, brain_settings)
        self.q.put(pos)

    def get_next_agent(self):
        pos = self.q.get()
        while self.agents[pos[0]][pos[1]] is None:
            a = self.q.get()

        return a

    def kill_agent(self, target_pos):
        a = self.agents[target_pos[0]][target_pos[1]]
        self.agents[target_pos[0]][target_pos[1]] = None

        return a.energy

    def is_occupied(self, target_pos):
        return not self.agents[target_pos[0]][target_pos[1]]

    def make_a_move(self, agent_pos, step):
        new_pos = (agent_pos[0] + step[0], agent_pos[1] + step[1])

        if new_pos[0] < 0 or new_pos[0] > self.width:
            raise AttributeError

        if new_pos[1] < 0 or new_pos[1] > self.height:
            raise AttributeError

        if abs(agent_pos[0] - new_pos[0]) > self.radius or abs(agent_pos[1] - new_pos[1]) > self.radius:
            raise AttributeError

        return new_pos

    def photosyn(self, agent):
        agent.energy = min(255, (agent.energy + self.photosyn_nrg))

    def eat(self, agent, target_pos):
        if abs(agent.pos[0] - target_pos[0]) > self.radius or abs(agent.pos[1] - target_pos[1]) > self.radius:
            raise AttributeError

        if not self.is_occupied(target_pos):
            agent.energy = min(agent.energy + self.field[target_pos[0], target_pos[1]].get_food(), 255)
        else:
            received_energy = self.kill_agent(target_pos)
            agent.energy = min(255, agent.energy + received_energy)
            self.agents[agent.pos[0]][agent.pos[1]] = None
            self.agents[target_pos[0]][target_pos[1]] = agent

    def get_info(self, agent_pos, target_pos):
        if abs(agent_pos[0] - target_pos[0]) > self.radius or abs(agent_pos[1] - target_pos[1]) > self.radius:
            raise AttributeError

        is_occupied = self.is_occupied(target_pos)
        is_food_here = self.field[target_pos[0], target_pos[1]].is_food_here()

        return tuple(is_occupied, is_food_here)
