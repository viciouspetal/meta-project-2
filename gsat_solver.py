import random as rd
import sys

import numpy as np

from ParseInstance import ParseInstance


class GsatSolver:
    # maintains a tabu list throughout the runs
    tabu = []
    max_tabu_elements = 5

    def main(self, max_restarts=10, max_iterations=1000, instance_path="./sat_data/test.cnf", experiment_count=1):
        # self.simple_solution(instance_path)
        parser = ParseInstance()
        instance = parser.readInstance(instance_path)
        var_count = len(instance[0])

        #print("~ experiment {0} ~".format(experiment_count))
        for restart in range(max_restarts):
            #print("#### restart {0} ###".format(restart))
            best_solution = self.initialize_variables(var_count)
            # print("initial best solution: {0}".format(best_solution))

            best_no_of_unsat_clauses = var_count

            for iteration in range(max_iterations):
                for i in range(var_count):
                    position_of_var_to_flip = i
                    var_to_flip = best_solution[position_of_var_to_flip]

                    if self.is_var_tabu(position_of_var_to_flip):
                        continue

                    best_solution[position_of_var_to_flip] = self.flip_var(var_to_flip)

                    solution_status, no_of_unsat_clauses = parser.solutionStatus(instance,
                                                                                 self.format_solution(best_solution))

                    # if solution has been found terminate the search
                    if solution_status:
                        print("Solution found at iteration: {0}, during {1} restart."
                              "\tSolution is: {2}".format(iteration, restart, best_solution))
                        return

                    # if solution hasn't been found check if proposed temp solution is better than previous best
                    if no_of_unsat_clauses < best_no_of_unsat_clauses:
                        best_no_of_unsat_clauses = no_of_unsat_clauses

                        # add current selection to tabu list
                        self.add_to_tabu(position_of_var_to_flip)
                        #print("Best solution so far: {0}, unsat {1}".format(best_solution, no_of_unsat_clauses))
                        #print("tabu list {0}".format(GsatSolver.tabu))
                    else:
                        # reversing the var flip as it did not improve the solution
                        best_solution[position_of_var_to_flip] = self.flip_var(best_solution[position_of_var_to_flip])

            # resetting tabu list in between the restarts
            GsatSolver.tabu = []

    def simple_solution(self, instance_path):
        """
        Simple solution without tabu search implemented.
        :param instance_path: path to formula file
        """
        parser = ParseInstance()
        instance = parser.readInstance(instance_path)
        # printIfDebugOn("instance {0}".format(instance), debug)
        print("instance {0}".format(instance))
        var_count = len(instance[0])
        variables = self.initialize_variables(var_count)
        print(variables)
        formattedSol = self.format_solution(variables)
        status = parser.solutionStatus(instance, formattedSol)
        iter_count = 0
        while not status:
            self.randomly_flip_variable(variables)
            formattedSol = self.format_solution(variables)
            status = parser.solutionStatus(instance, formattedSol)
            iter_count = iter_count + 1
        print("Solution found after {0} iterations. \n Solution is: {1}".format(iter_count, formattedSol))

    def randomly_flip_variable(self, variables):
        """
        Flips a random variable.
        :param variables: List of available variables
        :return: list of available variables with only 1 of the variables flipped to opposing value
        """
        max_var = len(variables) - 1

        # get position and variable to flip at random
        position_of_var_to_flip = self.get_flip_position(max_var)
        var_to_flip = variables[position_of_var_to_flip]

        # check if variable chosen is part of the tabu list
        while self.is_var_tabu(position_of_var_to_flip):
            position_of_var_to_flip = self.get_flip_position(max_var)
            var_to_flip = variables[position_of_var_to_flip]

        # add current selection to tabu list
        self.add_to_tabu(position_of_var_to_flip)

        # flip the variable
        variables[position_of_var_to_flip] = self.flip_var(var_to_flip)

        return variables, position_of_var_to_flip

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

    def get_flip_position(self, maxPosition):
        return rd.randint(0, maxPosition)

    def is_var_tabu(self, variable):
        """
        Checks if a given variable is part of the tabu list
        :param variable: variable to be checked against tabu list
        :return: true if given variable is contained in tabu list. Otherwise false.
        """

        # print("Tabu list has {0} elements. Tabu list is: {1}. Var {2} is in tabu list {3}". format(len(GsatSolver.tabu),
        # GsatSolver.tabu, variable, variable in GsatSolver.tabu))

        # TODO need to redesign it to maybe be a dictionary
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
        return np.random.randint(2, size=count)

    def format_solution(self, solution_proposed):
        """
        Proposed solution needs to be presented for further processing in a dictionary format, where the key is the
        position of the variable and the value is the 0 or 1 value of the variable
        :param solution_proposed: solution proposed in list format
        :return: solution proposed in dictionary format
        """
        tmp = {}
        for var in range(0, len(solution_proposed)):
            tmp[var + 1] = solution_proposed[var]

        return tmp


if __name__ == '__main__':
    solver = GsatSolver()

    if len(sys.argv) > 1:
        for i in range(5):
            solver.main(10, 1000, sys.argv[1], i)
    else:
        solver.main()


    # solution_status, no_of_unsat_clauses = parser.solutionStatus(instance,
    #                                                              self.format_solution(best_solution))
    #
    # # if solution has been found terminate the search
    # if solution_status:
    #     print("Solution found at iteration: {0}, during {1} restart."
    #           "\tSolution is: {2}".format(iteration, restart, best_solution))
    #     return
    #
    # # if solution hasn't been found check if proposed temp solution is better than previous best
    # if no_of_unsat_clauses < best_no_of_unsat_clauses:
    #     best_no_of_unsat_clauses = no_of_unsat_clauses
    # else:
    #     # reversing the var flip as it did not improve the solution
    #     best_solution[flipped_position] = self.flip_var(best_solution[flipped_position])
    #
    #     # print("Current best no of unsat {0}, proposed best no of unsat {1}, best solution {2}". format(best_no_of_unsat_clauses, no_of_unsat_clauses, best_solution))
