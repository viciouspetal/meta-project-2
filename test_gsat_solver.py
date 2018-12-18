import unittest
from gsat_solver import GsatSolver

class TestGsatSolver(unittest.TestCase):
    def test_pop_method(self):
        test_list = []

        for i in range(0,10):
            test_list.append(i)

        self.assertEqual(10, len(test_list))
        print(test_list)
        test_list.pop(0)

        print(test_list)

        self.assertEqual(9, len(test_list))
        self.assertEqual(1, test_list[0])

    def test_adding_to_tabu_limit(self):
        obj_under_test = GsatSolver()
        obj_under_test.max_tabu_elements=2
        pass


if __name__ == '__main__':
    unittest.main()