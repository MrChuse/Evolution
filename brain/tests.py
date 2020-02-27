from interpreterBrain import InterpreterBrain
from randomBrain import RandomBrain
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
    move = (1, True) # id = 1
    unconditional_jump = (1, False, lambda x, y: y[1])
    check_field = (3, False, lambda x, y: y[2] if x[y[1]]%2 == 0 else y[3])
    commands = [photosynthesis, move, unconditional_jump, check_field]
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

if __name__ == '__main__':
    unittest.main()
