import sys
import time

from SatUtils import SatUtils


class GsatSolver:
    # maintains a tabu list throughout the runs
    tabu = []
    max_tabu_elements = 5

    def main(self, max_restarts=10, max_iterations=1000, instance_path="./sat_data/test.cnf"):
        instance = SatUtils.read_instance(instance_path)
        var_count = len(instance[0])

        start = time.time()
        end = None

        for restart in range(max_restarts):
            best_solution = SatUtils.initialize_variables(var_count)

            for iteration in range(max_iterations):
                solution_status, no_of_unsat_clauses = SatUtils.solution_status(instance, best_solution)

                # if solution has been found terminate the search
                if solution_status is True:
                    end = time.time()

                    print(
                        "Iteration,{0},Restart,{1},Duration,{2}".format(iteration, restart, end - start))
                    return
                best_solution = self.get_best_var_to_flip(instance, best_solution, no_of_unsat_clauses)

            # resetting tabu list in between the restarts
            GsatSolver.tabu = []

    def get_best_var_to_flip(self, instance, best_solution, current_no_of_unsat_clauses):
        best_no_of_unsat_clauses = current_no_of_unsat_clauses
        best = best_solution.copy()
        utils = SatUtils()

        for i in range(1, len(best)):
            # checking if given variable is part of tabu list. If it is then next var is selected for the flip
            if self.is_var_tabu(i):
                continue

            tmp_solution = best_solution.copy()
            # working copy of the proposed solution
            var_to_flip = tmp_solution[i]

            # flipping a selected variable to opposing value
            tmp_solution[i] = SatUtils.flip_var(var_to_flip)

            _, no_of_unsat_clauses = SatUtils.solution_status(instance, tmp_solution)

            # if solution hasn't been found check if proposed temp solution is better than previous best
            if no_of_unsat_clauses < best_no_of_unsat_clauses:
                best_no_of_unsat_clauses = no_of_unsat_clauses

                # add current selection to tabu list
                self.add_to_tabu(i)
                # remember the best solution found so far for the next iteration
                best = tmp_solution.copy()

        return best

    def is_var_tabu(self, variable):
        """
        Checks if a given variable is part of the tabu list
        :param variable: variable to be checked against tabu list
        :return: true if given variable is contained in tabu list. Otherwise false.
        """

        return variable in GsatSolver.tabu

    def add_to_tabu(self, position_to_tabu):
        """
        Maintains a tabu list. If the number of tabu list elements is under the specified limit then simply adds
        the new variable position to the list.
        Otherwise, if the max number of elements in tabu list is reached it removes the oldest restriction -
        which corresponds to the first element in the list
        :param position_to_tabu: index, or position of a variable to be restricted
        """
        if len(GsatSolver.tabu) == GsatSolver.max_tabu_elements:
            GsatSolver.tabu.pop(0)

        GsatSolver.tabu.append(position_to_tabu)


if __name__ == '__main__':
    instance_path = None

    # check whether a path to input dataset has been provided or should the default path be used
    if len(sys.argv) > 1:
        instance_path = sys.argv[1]
    else:
        instance_path = "./sat_data/uf20-020.cnf"

    solver = GsatSolver()
    solver.main(10, 1000, instance_path)

