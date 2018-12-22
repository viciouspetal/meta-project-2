import unittest
import heapq
import random

from SatUtils import SatUtils

class TestSolversAndUtils(unittest.TestCase):
    def test_pop_method(self):
        test_list = []

        for i in range(0,10):
            test_list.append(i)

        self.assertEqual(10, len(test_list))
        print(test_list)
        test_list.pop(0)


        self.assertEqual(9, len(test_list))
        self.assertEqual(1, test_list[0])

    def test_dictionary_sorting(self):
        scores={5: 16, 6: 16, 2: 17, 18: 17, 10: 17, 12: 17, 7: 13, 4: 12, 13: 13, 1: 15, 17: 15, 19: 17, 14: 14, 3: 14, 9: 14, 11: 14, 16: 13, 8: 13, 15: 13, 20: 13}
        two_smallest = heapq.nsmallest(2, scores, key=scores.get)

        self.assertIn(7, two_smallest)
        self.assertIn(4, two_smallest)
        self.assertEqual(4,two_smallest[0])
        self.assertEqual(7,two_smallest[1])

    def test_randomly_picking_variable_from_clause(self):
        unsat_clause_list = [[5, -6, 2], [-18, -10, 12], [1, 17, -6], [2, -16, 4], [15, 12, -3], [1, 2, -6], [-19, 5, 2], [9, 2, -6], [-6, 2, 4], [-6, 1, -18], [5, 13, 15], [9, -10, 13], [13, 1, -16], [-14, 17, 5], [11, 8, 1], [17, 20, 4], [-19, 1, 2], [8, -10, 12], [13, -10, -16]]

        choice_clause = random.choice(unsat_clause_list)
        choice_var = random.choice(choice_clause)

        self.assertGreater(abs(choice_var), 0)

    def test_flip_var(self):
        utils = SatUtils()

        result = utils.flip_var(0)

        self.assertEquals(1, result)

if __name__ == '__main__':
    unittest.main()