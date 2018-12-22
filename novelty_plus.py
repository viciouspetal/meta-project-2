import random
import sys
import time

from SatUtils import SatUtils
from noveltysearch import NoveltySearch
from walk_sat import WalkSat


class NoveltyPlus:

    def main(self, wp, p, max_iterations, instance_path):
        cnf_contents = SatUtils.read_instance(instance_path)
        # instantiate required search and util objects
        novelty_search = NoveltySearch(cnf_contents, p, 1)
        variables = cnf_contents[0]
        walkSat = WalkSat()

        # initialize first solution proposal
        proposed_solution = SatUtils.initialize_variables(len(variables))

        # start the timer
        start = time.time()
        end = None

        for i in range(max_iterations):
            # checking for timeout terminate condition
            if time.time() > start + 60:
                return
            solution_found, unsat_clause, unsat_clause_list = SatUtils.solution_status_with_unsat_clauses(cnf_contents,
                                                                                                          proposed_solution)
            # if a solution has been identified break out of the search loop and record it
            if solution_found is True:
                end = time.time()
                print("Iteration,{0},Duration,{1}".format(i, end - start))
                return

            # pick algorithm to run the solution search based on probability
            if wp < random.uniform(0, 1):
                proposed_solution = walkSat.execute_walk(cnf_contents, proposed_solution)
            else:
                random_variable_to_flip = random.choice(variables)
                random_unsat_clause = random.choice(unsat_clause_list)

                best_flip = novelty_search.execute_search(proposed_solution, random_variable_to_flip,
                                                          random_unsat_clause)

                proposed_solution[best_flip] = SatUtils.flip_var(proposed_solution[best_flip])


if __name__ == '__main__':
    instance_path = None

    # check whether a path to input dataset has been provided or should the default path be used
    if len(sys.argv) > 1:
        instance_path = sys.argv[1]
    else:
        instance_path = "./sat_data/uf20-020.cnf"

    solver = NoveltyPlus()

    for experiment in range(1):
        solver.main(wp=0.4, p=0.3, max_iterations=100000, instance_path=instance_path)
