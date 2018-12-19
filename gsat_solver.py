import sys
import time

import numpy as np

from ParseInstance import ParseInstance


class GsatSolver:
    # maintains a tabu list throughout the runs
    tabu = []
    max_tabu_elements = 5

    def main(self, max_restarts=10, max_iterations=1000, instance_path="./sat_data/test.cnf", experiment_count=1):
        parser = ParseInstance()
        instance = parser.readInstance(instance_path)
        var_count = len(instance[0])

        # print("~ experiment {0} ~".format(experiment_count))
        start = time. time()
        end = None
        for restart in range(max_restarts):
            #print("#### restart {0} ###".format(restart))
            best_solution = self.initialize_variables(var_count)
            # print("initial best solution: {0}".format(best_solution))

            best_no_of_unsat_clauses = var_count

            for iteration in range(max_iterations):
                # if solution has been found terminate the search
                for i in range(1, var_count + 1):
                    position_of_var_to_flip = i
                    var_to_flip = best_solution[position_of_var_to_flip]

                    if self.is_var_tabu(position_of_var_to_flip):
                        continue

                    best_solution[position_of_var_to_flip] = self.flip_var(var_to_flip)

                    solution_status, no_of_unsat_clauses = parser.solutionStatus(instance, best_solution)

                    if solution_status:
                        end = time. time()

                        print("Iteration,{0},Restart,{1},Duration,{2}".format(iteration, restart, end - start))
                        return
                    # if solution hasn't been found check if proposed temp solution is better than previous best
                    if no_of_unsat_clauses < best_no_of_unsat_clauses:
                        best_no_of_unsat_clauses = no_of_unsat_clauses

                        # add current selection to tabu list
                        self.add_to_tabu(position_of_var_to_flip)
                    # print("Best solution so far: {0}, unsat {1}".format(best_solution, no_of_unsat_clauses))
                    # print("tabu list {0}".format(GsatSolver.tabu))
                    else:
                        # reversing the var flip as it did not improve the solution
                        best_solution[position_of_var_to_flip] = self.flip_var(best_solution[position_of_var_to_flip])

            # resetting tabu list in between the restarts
            GsatSolver.tabu = []

    def flip_var(self, variable):
        """
        Simple utility method that flips a value of a variable to the opposite value, e.g. if variable passed in has value of 0 it returns 1 and vice versa
        :param variable: variable to be flipped
        :return: variable of opposing value
        """
        if variable == 0:
            variable = 1
        else:
            variable = 0
        return variable

    def is_var_tabu(self, variable):
        """
        Checks if a given variable is part of the tabu list
        :param variable: variable to be checked against tabu list
        :return: true if given variable is contained in tabu list. Otherwise false.
        """

        # tried with a dictionary to avoid a loop comprehension, however, dictionaries are sorted and do not persist
        # the ordering of which key, in our case which move was added as tabu, meaning it would be impossible to
        # determine which move was the oldest and should be removed when tabu limit was hit.
        return variable in GsatSolver.tabu

    def add_to_tabu(self, position_to_tabu):
        """
        Maintains a tabu list. If the number of tabu list elements is under the specified limit then simply adds
        the new variable position to the list.
        Otherwise, if the max number of elements in tabu list is reached it removes the oldest restriction -
        which corresponds to the first element in the list
        :param position_to_tabu: index, or position of a variable to be restricted
        """
        if len(GsatSolver.tabu) >= GsatSolver.max_tabu_elements:
            GsatSolver.tabu.pop(0)

        GsatSolver.tabu.append(position_to_tabu)

    def initialize_variables(self, count):
        """
        Initialize an array of a given size - defined by count parameter - with randomly assigned 0 or 1 values.
        :param count: size of the array to be initialized
        :return: Array initialized with randomly assigned 0 and 1 values
        """

        return dict(enumerate(np.random.randint(2, size=count), 1))

if __name__ == '__main__':
    solver = GsatSolver()

    if len(sys.argv) > 1:
        for i in range(100):
            solver.main(10, 1000, sys.argv[1], i)
    else:
        solver.main()




"the code you want to test stays here"

