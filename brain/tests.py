from interpreterBrain import InterpreterBrain
from randomBrain import RandomBrain
import nn
from nnBrain import nnBrain
import unittest


class RandomBrainTestCase(unittest.TestCase):

    def setUp(self):
        photosynthesis = (0, True) # id = 0
        move = (1, True) # id = 1
        self.commands = [photosynthesis, move]
        self.b = RandomBrain(self.commands, 10)

    def test_for_output(self):
        for i in range(100):
            a = self.b.make_a_move(None)
            if a == -1:
                self.assertTrue(True)
            else:
                self.assertEqual(self.commands[a[0]][0] + 1, len(a))


class InterpreterBrainTestCase(unittest.TestCase):

    photosynthesis = (0, True) # id = 0
    move = (1, True) # id = 1, 4, 5, 6
    unconditional_jump = (1, False, lambda x, y: y[1])
    check_field = (3, False, lambda x, y: y[2] if x[y[1]]%2 == 0 else y[3])
    commands = [photosynthesis, move, unconditional_jump, check_field, photosynthesis, photosynthesis, photosynthesis]
    command_limit = 10


    def buildBrain(self, data):
        return InterpreterBrain(self.commands, self.command_limit, data)

    def test_primitive_case(self):
        data = [0]
        self.b = self.buildBrain(data)
        for i in range(5):
            with self.subTest(i=i):
                a = self.b.make_a_move(None)
                self.assertEqual(a, [0])

    def test_without_final_commands(self):
        data = [3, 3, 3, 3]
        self.b = self.buildBrain(data)
        for i in range(5):
            with self.subTest(i=i):
                a = self.b.make_a_move(None)
                self.assertEqual(a, -1)

    def test_skip_large_numbers(self):
        data = [63, 0, 1, 60, 60, 0]
        self.b = self.buildBrain(data)
        for correct in ([0], [1, 60], [0]):
            self.subTest(correct=correct)
            a = self.b.make_a_move(None)
            self.assertEqual(a, correct)

    def test_unconditional_jump_with_final_command_without_parameters(self):
        data = [0, 2, 3, 1]
        self.b = self.buildBrain(data)
        for i in range(5):
            with self.subTest(i=i):
                a = self.b.make_a_move(None)
                self.assertEqual(a, [0])

    def test_unconditional_jump_with_final_command_without_parameters(self):
        data = [1, 2, 2, 2]
        self.b = self.buildBrain(data)
        for i in range(5):
            with self.subTest(i=i):
                a = self.b.make_a_move(None)
                self.assertEqual(a, [1, 2])

    def test_conditional_jump_with_sensor_data_lookup(self):
        data = [3, 0, 4, 5, 4, 5, 6]
        self.b = self.buildBrain(data)

        sensor_data = [0]
        for correct in ([4], [5], [6]):
            self.subTest(correct=correct, sensor_data=sensor_data)
            a = self.b.make_a_move(sensor_data)
            self.assertEqual(a, correct)

        sensor_data = [1]
        for correct in ([5], [6], [5], [6]):
            self.subTest(correct=correct, sensor_data=sensor_data)
            a = self.b.make_a_move(sensor_data)
            self.assertEqual(a, correct)


class nnBrainTestCase(unittest.TestCase):
    
    def setUp(self):        
        photosynthesis = (0, True) # id = 0
        move = (1, True) # id = 1
        self.commands = [photosynthesis, move]

        d = (nn.Dense, (10, 10))
        a = (nn.ReLU, set())
        parameters = (d, a)
        self.b = nnBrain(commands=self.commandsdata=(parameters,))

    def test_init(self):
        self.assertTrue(True)

    def test_make_a_move(self):
        pass

if __name__ == '__main__':
    unittest.main()
