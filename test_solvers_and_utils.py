import heapq
import random
import unittest

from sat_utils import SatUtils
from tsp_solver import TspSolver


class TestSolversAndUtils(unittest.TestCase):
    def test_pop_method(self):
        test_list = []

        for i in range(0, 10):
            test_list.append(i)

        self.assertEqual(10, len(test_list))
        test_list.pop(0)

        self.assertEqual(len(test_list), 9)
        self.assertEqual(test_list[0], 1)

    def test_dictionary_sorting(self):
        scores = {5: 16, 6: 16, 2: 17, 18: 17, 10: 17, 12: 17, 7: 13, 4: 12, 13: 13, 1: 15, 17: 15, 19: 17, 14: 14,
                  3: 14, 9: 14, 11: 14, 16: 13, 8: 13, 15: 13, 20: 13}
        two_smallest = heapq.nsmallest(2, scores, key=scores.get)

        self.assertIn(7, two_smallest)
        self.assertIn(4, two_smallest)
        self.assertEqual(4, two_smallest[0])
        self.assertEqual(7, two_smallest[1])

    def test_randomly_picking_variable_from_clause(self):
        unsat_clause_list = [[5, -6, 2], [-18, -10, 12], [1, 17, -6], [2, -16, 4], [15, 12, -3], [1, 2, -6],
                             [-19, 5, 2], [9, 2, -6], [-6, 2, 4], [-6, 1, -18], [5, 13, 15], [9, -10, 13], [13, 1, -16],
                             [-14, 17, 5], [11, 8, 1], [17, 20, 4], [-19, 1, 2], [8, -10, 12], [13, -10, -16]]

        choice_clause = random.choice(unsat_clause_list)
        choice_var = random.choice(choice_clause)

        self.assertGreater(abs(choice_var), 0)

    def test_flip_var(self):
        result = SatUtils.flip_var(0)

        self.assertEqual(result, 1)

    def test_initializing_variables(self):
        result = SatUtils.initialize_variables(10)

        print(result)

        self.assertEqual(len(result), 10)

    def test_read_instance(self):
        test_file_path = './sat_test_data/test.cnf'

        cnf = SatUtils.read_instance(test_file_path)
        self.assertEqual(len(cnf), 2)
        self.assertEqual(len(cnf[0]), 6)
        self.assertEqual(len(cnf[1]), 4)

    def test_basic_solution_status_with_false_state(self):
        formula = [[1, 2, 3, 4, 5, 6], [[1, -2, 3], [1, -2, -3], [1, 2, 4], [-4, -5, 6]]]

        solution = {1: 1, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0}

        solution_found, unsat_result = SatUtils.solution_status(formula, solution)
        self.assertFalse(solution_found)
        self.assertEqual(unsat_result, 1)

    def test_basic_solution_status_with_true_state(self):
        formula = [[1, 2, 3, 4, 5, 6], [[1, -2, 3], [1, -2, -3], [1, 2, 4], [-4, -5, 6]]]

        solution = {1: 1, 2: 1, 3: 0, 4: 1, 5: 1, 6: 1}

        solution_found, unsat_result = SatUtils.solution_status(formula, solution)
        self.assertTrue(solution_found)
        self.assertEqual(unsat_result, 0)

    def test_solution_status_with_false_state(self):
        formula = [[1, 2, 3, 4, 5, 6], [[1, -2, 3], [1, -2, -3], [1, 2, 4], [-4, -5, 6]]]

        solution = {1: 1, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0}

        solution_found, unsat_result, unsat_list = SatUtils.solution_status_with_unsat_clauses(formula, solution)
        self.assertFalse(solution_found)
        self.assertEqual(unsat_result, 1)
        self.assertEqual(len(unsat_list), 1)

    def test_solution_status_with_true_state(self):
        formula = [[1, 2, 3, 4, 5, 6], [[1, -2, 3], [1, -2, -3], [1, 2, 4], [-4, -5, 6]]]

        solution = {1: 1, 2: 1, 3: 0, 4: 1, 5: 1, 6: 1}

        solution_found, unsat_result, unsat_list = SatUtils.solution_status_with_unsat_clauses(formula, solution)
        self.assertTrue(solution_found)
        self.assertEqual(unsat_result, 0)
        self.assertEqual(len(unsat_list), 0)

    def test_generate_3_opt_swap(self):
        #filepath, max_iterations, local_search_time_limit, algorithm
        tour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        tsp = TspSolver(None, None, None, None)
        result = tsp.generate_3_opt_swap(2, 6, 9, tour)
        expected_result = [0, 1, 6, 5, 4, 3, 2, 9, 8, 7, 0]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
