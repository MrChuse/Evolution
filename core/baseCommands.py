def ucj(sensor_data, com_arg): # UnConditional Jump
    return com_arg[1]
def cha(sensor_data, com_arg): # CHeck Ally
    return com_arg[2] if sensor_data[0].agent.brain.check_ally(sensor_data[com_arg[1]].agent.brain) else com_arg[3]
def occ(sensor_data, com_arg): # is OCCupied
    return com_arg[2] if sensor_data[com_arg[1]].is_occupied() else com_arg[3]
def ifd(sensor_data, com_arg): # Is FooD present
    return com_arg[2] if sensor_data[com_arg[1]].is_food_here() else com_arg[3]
def ame(sensor_data, com_arg): # Amount of MEat
    return com_arg[3] if sensor_data[com_arg[1]].get_amount_of_meat() > com_arg[2] else com_arg[4]
def ami(sensor_data, com_arg): # Amount of MInerals
    return com_arg[3] if sensor_data[com_arg[1]].get_amount_of_minerals() > com_arg[2] else com_arg[4]
def tmp(sensor_data, com_arg): # TeMPerature Positive
    return com_arg[3] if sensor_data[com_arg[1]].get_temperature() > com_arg[2] else com_arg[4]
def tmn(sensor_data, com_arg): # TeMPerature Negative
    return com_arg[3] if sensor_data[com_arg[1]].get_temperature() > -com_arg[2] else com_arg[4]

photosynthesis         = (0, True)        # id = 0
move                   = (2, True)        # id = 1
eat                    = (3, True)        # id = 2
give_birth_to          = (3, True)        # id = 3
share_energy           = (3, True)        # id = 4
unconditional_jump     = (1, False, ucj)  # id = 5
check_ally             = (3, False, cha)  # id = 6
is_occupied            = (3, False, occ)  # id = 7
is_food_present        = (3, False, ifd)  # id = 8
compare_amt_meat       = (4, False, ame)  # id = 9
compare_amt_minerals   = (4, False, ami)  # id = 10
compare_tmp_pos        = (4, False, tmp)  # id = 11
compare_tmp_neg        = (4, False, tmn)  # id = 12

check_ally = (5, False, move_pointer_check_ally)
base_commands = [photosynthesis, move, eat, give_birth_to, share_energy, unconditional_jump,
                 check_ally, is_occupied, is_food_present, compare_amt_meat, compare_amt_minerals,
                 compare_tmp_pos, compare_tmp_neg]
