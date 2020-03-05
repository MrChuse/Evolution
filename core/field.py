class CellType:
    def __init__(self, type_number=0, food=0, temperature=0, energy_value=1):
        self.type_number = type_number
        self.food = food
        self.temperature = temperature
        self.energy_value = energy_value


class Cell:
    def __init__(self, cell_type=0, agent=None):
        self.cell_type = CellType(cell_type)
        self.agent = agent

    def is_occupied(self):
        return True if not self.agent else False


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        for i in range(width):
            for j in range(height):
                self.field[i][j] = Cell()
