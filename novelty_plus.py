import random
import time

from SatUtils import SatUtils
from noveltysearch import NoveltySearch
from walk_sat import WalkSat


class NoveltyPlus:

    def main(self, formula, wp, p, max_iterations):
        # instantiate required search and util objects
        novelty_search = NoveltySearch(formula, p, 1)
        variables = formula[0]
        walkSat = WalkSat()

        # initialize first solution proposal
        proposed_solution = SatUtils.initialize_variables(variables)

        # start the timer
        start = time.time()
        end = None

        for i in range(max_iterations):
            solution_found, unsat_clause, unsat_clause_list = SatUtils.solution_status_with_unsat_clauses(formula,
                                                                                                          proposed_solution)

            # if a solution has been identified break out of the search loop and record it
            if solution_found is True:
                end = time.time()
                print("Iteration,{0},Duration,{1}, Solution, {2}".format(i, end - start, proposed_solution))
                return

            # pick algorithm to run the solution search based on probability
            if wp < random.uniform(0, 1):
                proposed_solution = walkSat.execute_walk(formula, proposed_solution)
            else:
                random_variable_to_flip = random.choice(variables)
                random_unsat_clause = random.choice(unsat_clause_list)

                best_flip = novelty_search.execute_search(proposed_solution, random_variable_to_flip,
                                                          random_unsat_clause)

                proposed_solution[best_flip] = SatUtils.flip_var(proposed_solution[best_flip])


if __name__ == '__main__':
    instance_path = "./sat_data/uf20-020.cnf"

    wp = 0.4
    p = 0.3
    cnf_contents = SatUtils.read_instance(instance_path)
    solver = NoveltyPlus()

    for experiment in range(100):
        solver.main(cnf_contents, wp, p, 100000)
