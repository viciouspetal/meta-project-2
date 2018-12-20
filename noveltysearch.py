import heapq
import random
import time

from GsatUtils import GsatUtils


class NoveltySearch:

    def __init__(self, instance, formula_vars, probability, max_iterations=10000):
        self.instance = instance
        self.variables = formula_vars
        self.probability = probability
        self.max_iterations = max_iterations

    def main(self):
        utils = GsatUtils()
        proposed_solution = utils.initialize_variables(len(self.variables))

        start = time.time()
        end = None
        for i in range(self.max_iterations):
            solution_found, unsat_clause, unsat_clause_list = self.solution_status(self.instance, proposed_solution)
            random_flip = random.choice(self.variables)
            random_clause = random.choice(unsat_clause_list)

            print("Unsat clauses, {0}".format(unsat_clause))
            if solution_found is True:
                end = time.time()
                print("Iteration,{0},Duration,{2}, Solution, {3}".format(i, end - start, proposed_solution))
                return proposed_solution

            flip_this_index = self.execute_search(proposed_solution, random_flip, random_clause)

            # print("before flip {0}".format(proposed_solution[flip_this_index]))
            proposed_solution[flip_this_index] = utils.flip_var(proposed_solution[flip_this_index])
            # print("After flip {0}".format(proposed_solution[flip_this_index]))

    def execute_search(self, proposed_solution, currently_flipped_variable, random_clause):
        if currently_flipped_variable not in random_clause:
            return currently_flipped_variable
        else:
            return self.choose_var_to_flip(proposed_solution)

    def choose_var_to_flip(self, proposed_solution):
        """
        Chose best or second best variable to flip based on the probability provided
        :param proposed_solution:
        :return:
        """
        tmp_solution = proposed_solution.copy()
        flip_scores = {}
        utils = GsatUtils()
        for i in range(len(self.variables)):
            tmp_solution[i] = utils.flip_var(self.variables[i])
            _, unsat_clauses = utils.solution_status(self.instance, tmp_solution)

            flip_scores[self.variables[i]] = unsat_clauses

            tmp_solution[i] = utils.flip_var(self.variables[i])

        # Find best and second best - extremely efficient according to stack overflow
        sorted = heapq.nsmallest(2, flip_scores, key=flip_scores.get)

        best = sorted[0]
        second_best = sorted[1]

        noise_value = random.uniform(0, 1)

        if noise_value < self.probability:
            return second_best
        else:
            return best

    def solution_status(self, instance, sol):
        clause = instance[1]
        unsat_clause = 0
        unsat_clause_list = []
        for clause_i in clause:
            cStatus = False
            tmp = []
            for var in clause_i:
                if var < 0:
                    if (1 - sol[-var]) == 1:
                        cStatus = True
                    tmp.append([var, sol[-var]])
                else:
                    tmp.append([var, sol[var]])
                    if sol[var] == 1:
                        cStatus = True
            if not cStatus:
                unsat_clause += 1
                unsat_clause_list.append(clause_i)

        if unsat_clause > 0:
            return False, unsat_clause, unsat_clause_list
        return True, unsat_clause, unsat_clause_list


if __name__ == '__main__':
    instance_path = "./sat_data/uf20-020.cnf"

    utils = GsatUtils()
    cnf_contents = utils.read_instance(instance_path)
    solver = NoveltySearch(cnf_contents, cnf_contents[0], 0.4, 100000)

    solver.main()
