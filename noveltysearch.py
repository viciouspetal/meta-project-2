import heapq
import random
import time
import sys

from SatUtils import SatUtils


class NoveltySearch:

    def __init__(self, instance, probability, max_iterations=10000):
        self.instance = instance
        self.variables = instance[0]
        self.probability = probability
        self.max_iterations = max_iterations

    def main(self):
        proposed_solution = SatUtils.initialize_variables(self.variables)

        start = time.time()
        end = None
        for i in range(self.max_iterations):
            solution_found, unsat_clause, unsat_clause_list = SatUtils.solution_status_with_unsat_clauses(self.instance,
                                                                                                          proposed_solution)

            if solution_found is True:
                end = time.time()
                print("Iteration,{0},Duration,{1}".format(i, end - start))
                return

            random_flip = random.choice(self.variables)
            random_clause = random.choice(unsat_clause_list)

            flip_this_index = self.execute_search(proposed_solution, random_flip, random_clause)

            proposed_solution[flip_this_index] = SatUtils.flip_var(proposed_solution[flip_this_index])

    def execute_search(self, proposed_solution, currently_flipped_variable, random_clause):
        """
        Choose a variable to be flipped.
        If a randomly chosen variable is present in the randomly selected unsatisfied clause then return that variable.
        Otherwise find best and second best variable to be flipped. The choice between which variable to select, best
        or second best is made based on the probability provided.
        :param proposed_solution:
        :return:
        """
        if currently_flipped_variable not in random_clause:
            return currently_flipped_variable
        else:
            # Chose best or second best variable to flip based on the probability provided
            tmp_solution = proposed_solution.copy()
            flip_scores = {}
            utils = SatUtils()

            # loop over the variables to see which flip generates the lowest number of unsatisfied clauses
            for i in range(len(self.variables)):
                tmp_solution[i] = SatUtils.flip_var(self.variables[i])
                _, unsat_clauses = SatUtils.solution_status(self.instance, tmp_solution)

                # keep track of which variable flip generated what number of unsatisfied clauses
                flip_scores[self.variables[i]] = unsat_clauses

                # flip the selected variable
                tmp_solution[i] = SatUtils.flip_var(self.variables[i])

            # Find best and second best - extremely efficient according to stack overflow
            two_smallest_keys = heapq.nsmallest(2, flip_scores, key=flip_scores.get)

            best = two_smallest_keys[0]
            second_best = two_smallest_keys[1]

            # generate noise value
            noise_value = random.uniform(0, 1)

            # compare noise value generated to the probability of second best variable being selected
            if noise_value < self.probability:
                return second_best
            else:
                return best


if __name__ == '__main__':
    instance_path = None

    # check whether a path to input dataset has been provided or should the default path be used
    if len(sys.argv) > 1:
        instance_path = sys.argv[1]
    else:
        instance_path = "./sat_data/uf20-020.cnf"

    cnf_contents = SatUtils.read_instance(instance_path)
    solver = NoveltySearch(cnf_contents, 0.4, 100000)

    for i in range(1):
        solver.main()
