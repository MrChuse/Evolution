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
    is_occupied
        says whether the cell is occupied (bool)
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

    def is_occupied(self):
        return not self.agent

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
    width : int
        field width
    height : int
        field height
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        for i in range(width):
            for j in range(height):
                self.field[i][j] = Cell()
