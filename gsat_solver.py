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

        print("~ experiment {0} ~".format(experiment_count))
        start = time. time()
        end = None

        for restart in range(max_restarts):
            # print("#### restart {0} ###".format(restart))
            best_solution = self.initialize_variables(var_count)
            GsatSolver.tabu = []

            #print(best_solution)
            for iteration in range(max_iterations):
                solution_status, no_of_unsat_clauses = self.solutionStatus(instance, best_solution)

                # if solution has been found terminate the search
                if solution_status is True:
                    end = time. time()

                    print("Iteration,{0},Restart,{1},Duration,{2}".format(iteration, restart, end - start))
                    return
                best_solution = self.get_best_var_to_flip(instance, best_solution, no_of_unsat_clauses)


            # resetting tabu list in between the restarts


    def get_best_var_to_flip(self, instance, best_solution, current_no_of_unsat_clauses):
        best_no_of_unsat_clauses = current_no_of_unsat_clauses
        best = best_solution.copy()

        for i in range(1, len(best)):
            # checking if given variable is part of tabu list. If it is then next var is selected for the flip
            if self.is_var_tabu(i):
                 continue

            tmp_solution = best_solution.copy()
            # working copy of the proposed solution
            var_to_flip = tmp_solution[i]

            tmp_solution[i] = self.flip_var(var_to_flip)

            _, no_of_unsat_clauses = self.solutionStatus(instance, tmp_solution)

            # if solution hasn't been found check if proposed temp solution is better than previous best
            if no_of_unsat_clauses < best_no_of_unsat_clauses:
                best_no_of_unsat_clauses = no_of_unsat_clauses

                # add current selection to tabu list
                self.add_to_tabu(i)
                best = tmp_solution.copy()

        return best

    def flip_var(self, variable):
        """
        Flips a value of a variable to the opposite value, e.g. if variable passed in has value of 0 it returns 1 and vice versa
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
        if len(GsatSolver.tabu) == GsatSolver.max_tabu_elements:
            GsatSolver.tabu.pop(0)

        GsatSolver.tabu.append(position_to_tabu)

    def initialize_variables(self, count):
        """
        Initialize a dictionary of a given size - defined by count parameter - with randomly assigned 0 or 1 values.
        :param count: the number of variables to be initialized
        :return: a dictionary initialized with randomly assigned 0 and 1 values
        """

        return dict(enumerate(np.random.randint(2, size=count), 1))

    def solutionStatus(self, instance, sol):
        #print("Instance: {0}\n instance[1]: {1}\n solution: {2}".format(instance, instance[1], sol))
        clause = instance[1]
        unsat_clause = 0
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
        if unsat_clause > 0:
            #print("UNSAT Clauses: {0}".format(unsat_clause))
            return False, unsat_clause
        return True, unsat_clause

if __name__ == '__main__':
    solver = GsatSolver()

    if len(sys.argv) > 1:
        for i in range(10):
            solver.main(10, 1000, sys.argv[1], i)
    else:
        for i in range(10):
            solver.main(experiment_count=1)
