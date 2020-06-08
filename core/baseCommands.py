def move_pointer_check_ally(sensor_data, command_and_arguments):
    return command_and_arguments[2] if brain.check_ally(other) else command_and_arguments[3]

# is_occupied = self.is_occupied(target_pos)
# is_food_here = self.field[target_pos[0]][target_pos[1]].is_food_here()
# amount_of_meat = self.field[target_pos[0]][target_pos[1]].get_amount_of_meat()
# amount_of_minerals = self.field[target_pos[0]][target_pos[1]].get_amount_of_minerals()
# temperature = self.field[target_pos[0]][target_pos[1]].get_temperature()

photosynthesis = (0, True)  # id = 0
move = (2, True)  # id = 1
eat = (3, True)  # id = 2
give_birth_to = (3, True)  # id = 3
share_energy = (3, True)  # id = 4
unconditional_jump = (1, False, lambda sensor_data, command_and_arguments: command_and_arguments[1])

check_ally = (5, False, move_pointer_check_ally)
base_commands = [photosynthesis, move, eat, give_birth_to, share_energy, unconditional_jump]
