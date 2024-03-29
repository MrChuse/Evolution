from Agent import Agent
import random, sys
import perlin

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

    def __init__(self, type_number=0, meat=0, minerals=0, temperature=0):
        self.type_number = type_number
        self.meat = meat
        self.minerals = minerals
        self.temperature = temperature
        self.meat_energy_value = 7 - (self.temperature - 1) // 8
        self.mineral_energy_value = (self.temperature - 1) // 8 + 8


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

    def __init__(self, cell_type=0, temperature=0, agent=None):
        self.cell_type = CellType(cell_type, temperature=temperature)
        self.agent = agent
        self.photosyn_nrg = self.cell_type.temperature // 12 + 6
        
    def is_occupied(self):
        return self.agent is not None

    def is_food_here(self):
        return self.cell_type.meat > 0 | self.cell_type.minerals > 0

    def is_meat_here(self):
        return self.cell_type.meat > 0

    def is_minerals_here(self):
        return self.cell_type.minerals > 0

    def get_meat(self):
        if not self.is_meat_here():
            return 0

        self.cell_type.meat -= 1
        return self.cell_type.meat_energy_value

    def get_mineral(self):
        if not self.is_minerals_here():
            return 0

        self.cell_type.minerals -= 1
        return self.cell_type.mineral_energy_value

    def get_amount_of_meat(self):
        return self.cell_type.meat

    def get_amount_of_minerals(self):
        return self.cell_type.minerals

    def get_temperature(self):
        return self.cell_type.temperature

    def get_cell_type(self):
        return self.cell_type.type_number

    def add_mineral(self):
        self.cell_type.minerals = min(self.cell_type.minerals + 1, 127)

    def add_meat(self, amount):
        self.cell_type.meat += amount


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
    
    def __init__(self, width=48, height=48, seed=None):
        self.width = width
        self.height = height
        self.share_penalty = 0.9
        self.q = []

        self.agents = []
        self.field = []

        if seed is None:
            seed = random.randrange(sys.maxsize)
        self.rng = random.Random(seed)
        print("Seed is:", seed)

        self.mineral_spawn_probability = 0.001

        self.noise = perlin.SimplexNoise(randint_function=self.rng.randint)
        self.noise_x = 0
        for i in range(width):
            self.agents.append([])
            self.field.append([])
            for j in range(height):
                temperature = int(self.from_noise_to_temperature(self.noise.noise2(self.noise_x, j / height)))
                c = Cell(temperature=temperature)
                # c.cell_type.temperature = - (j / self.height * 128) + 64
                self.field[i].append(c)
                self.agents[i].append(None)
            self.noise_x += 1 / width

    @staticmethod
    def from_noise_to_temperature(t):
        return 64 * t

    def move_field(self):
        for index, pos in enumerate(self.q):
            self.q[index] = pos[0] - 1, pos[1]
            self.field[pos[0]][pos[1]].agent.pos = pos[0] - 1, pos[1]
        for pos in reversed(self.q):
            if pos[0] < 0:
                self.q.remove(pos)
        #print(self.q)
        self.field = self.field[1:]
        self.field.append([])
        for i in range(self.width):
            temperature = int(self.from_noise_to_temperature(self.noise.noise2(self.noise_x, i / self.height)))
            self.field[-1].append(Cell(temperature=temperature))
        self.noise_x += 1 / self.width

    def spawn_agent(self, pos, brain_settings, energy=50, energy_cap=255, radius=1, brain_type='interpreter'):
        self.field[pos[0]][pos[1]].agent = Agent(pos, energy, energy_cap, radius, brain_type, brain_settings)
        self.q.append(pos)

    def kill_agent(self, target_pos):
        # let's imagine that someone very bad tried to kill an unexisting agent. Wooooow! We've stopped him!!!!!!!
        if self.q.count(target_pos) > 0:
            received_energy = self.field[target_pos[0]][target_pos[1]].agent.energy
            self.q.remove(target_pos)
            self.field[target_pos[0]][target_pos[1]].agent = None

            return max(0, received_energy)
        return 0

    def make_a_move(self, agent, new_pos, index):
        if new_pos[0] < 0 or new_pos[0] >= self.width:
            return agent.pos

        if new_pos[1] < 0 or new_pos[1] >= self.height:
            return agent.pos

        if abs(agent.pos[0] - new_pos[0]) > agent.radius or abs(agent.pos[1] - new_pos[1]) > agent.radius:
            return agent.pos

        if self.field[new_pos[0]][new_pos[1]].is_occupied():
            return agent.pos

        agent.energy -= 8 * max(abs(agent.pos[0] - new_pos[0]), abs(agent.pos[1] - new_pos[1]))
        self.field[agent.pos[0]][agent.pos[1]].agent = None
        agent.pos = new_pos
        self.field[new_pos[0]][new_pos[1]].agent = agent
        self.q[index] = new_pos

        return agent.pos

    def photosyn(self, agent):
        agent.eats['photo'] += 1
        agent.clamp_eats()
        agent.energy += self.field[agent.pos[0]][agent.pos[1]].photosyn_nrg

    def eat(self, agent, target_pos, index):
        if agent.pos == target_pos:
            return

        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if abs(agent.pos[0] - target_pos[0]) > agent.radius or abs(agent.pos[1] - target_pos[1]) > agent.radius:
            return

        if not self.field[target_pos[0]][target_pos[1]].is_occupied():
            agent.eats['meat'] += 1
            agent.clamp_eats()
            agent.energy += self.field[target_pos[0]][target_pos[1]].get_meat()
        else:
            agent.energy -= 4
            received_energy = self.kill_agent(target_pos)
            self.field[target_pos[0]][target_pos[1]].add_meat(received_energy // 8)

    def eat_mineral(self, agent, target_pos):
        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if abs(agent.pos[0] - target_pos[0]) > agent.radius or abs(agent.pos[1] - target_pos[1]) > agent.radius:
            return

        agent.eats['minerals'] += 1
        agent.clamp_eats()
        agent.energy += self.field[target_pos[0]][target_pos[1]].get_mineral()

    def get_info(self, agent, target_pos):
        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if abs(agent.pos[0] - target_pos[0]) > agent.radius or abs(agent.pos[1] - target_pos[1]) > agent.radius:
            return

        return self.field[target_pos[0]][target_pos[1]]

    def get_sensor_data(self, agent):
        sensor_data = [self.get_info(agent, agent.pos)]
        for r in range(1, agent.radius + 1):
            for d in range(2 * r):
                for di, dj in ((-r+d, -r), (r, -r+d), (r-d, r), (-r, r-d)):
                    if ((agent.pos[0] + di) < 0 or (agent.pos[0] + di) >= self.width or
                            (agent.pos[1] + dj) < 0 or (agent.pos[1] + dj) >= self.height):
                        sensor_data.append(None)
                        continue
                    sensor_data.append(self.get_info(agent, (agent.pos[0] + di, agent.pos[1] + dj)))
        return sensor_data

    def give_birth_to(self, agent, target_pos, energy, brain_settings, mutation_settings):
        if agent.energy < energy:
            return

        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        if self.field[target_pos[0]][target_pos[1]].is_occupied():
            if self.field[agent.pos[0]][agent.pos[1]] is None:
                print('cant give birth and None, harakiri', agent.pos[0], agent.pos[1], self.field[agent.pos[0]][agent.pos[1]])
            self.kill_agent(agent.pos)
            return

        self.spawn_agent(target_pos, brain_settings, energy)
        agent.energy -= energy

        # self.agents[target_pos[0]][target_pos[1]].mutate(self.rng, mutation_settings)
        self.field[target_pos[0]][target_pos[1]].agent.mutate(self.rng, mutation_settings)

    def give_birth_random(self, agent, brain_settings, mutation_settings):
        dx = int(self.rng.random() * (2 * agent.radius + 1))
        dy = int(self.rng.random() * (2 * agent.radius + 1))
        energy = int(max(self.rng.random() * agent.energy, agent.energy / 2))
        self.give_birth_to(agent, (agent.pos[0] + dx, agent.pos[1] + dy), energy, brain_settings, mutation_settings)

    def do_nothing(self):
        pass

    def temperature_effect(self, agent):
        if not agent.alive:
            return

        t = self.field[agent.pos[0]][agent.pos[1]].get_temperature()
        agent.energy -= abs(t) // 10

    def brain_size_effect(self, agent):
        if not agent.alive:
            return

        brain_size = agent.get_brain_size()
        if brain_size <= 64:
            agent.energy -= round(0.5 * brain_size ** 0.5)
        else:
            agent.energy -= ((brain_size - 64) ** 2) // 5 + 4

    def share_energy(self, agent, target_pos, amount_of_energy):
        if agent.energy < amount_of_energy:
            return

        if target_pos[0] < 0 or target_pos[0] >= self.width:
            return

        if target_pos[1] < 0 or target_pos[1] >= self.height:
            return

        # if self.agents[target_pos[0]][target_pos[1]] is None:
        if self.field[target_pos[0]][target_pos[1]].agent is None:
            return

        if abs(agent.pos[0] - target_pos[0]) > agent.radius or abs(agent.pos[1] - target_pos[1]) > agent.radius:
            return

        # target_agent = self.agents[target_pos[0]][target_pos[1]]
        target_agent = self.field[target_pos[0]][target_pos[1]].agent
        new_amount = min(amount_of_energy, target_agent.energy_cap - target_agent.energy)
        agent.energy -= new_amount
        target_agent.energy += int(new_amount * self.share_penalty)

    def add_minerals(self):
        for row in self.field:
            for cell in row:
                if self.rng.random() < self.mineral_spawn_probability:
                    cell.add_mineral()
