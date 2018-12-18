import random as rd
import sys

import numpy as np

from ParseInstance import ParseInstance


class GsatSolver:

    def main(self, max_restarts=10, max_iterations=1000, instance_path="./sat_data/test.cnf"):
        # self.simple_solution(instance_path)
        parser = ParseInstance()
        instance = parser.readInstance(instance_path)
        var_count = len(instance[0])
        best_solution = self.initialize_variables(var_count)
        print("best solution: ", best_solution)

        for restart in range(max_restarts):
            best_no_of_unsat_clauses = var_count
            tmp_best_solution = best_solution
            currently_best_solution = tmp_best_solution

            for iteration in range(max_iterations):
                # generate a random temp solution to work on
                tmp_solution = tmp_best_solution
                #print("tmp solution",tmp_solution)
                #print("Before flip: {0}".format(tmp_solution))
                # flip the variables at random
                self.flip_variable(tmp_solution)
                #print("After flip: {0}".format(tmp_solution))

                solution_status, no_of_unsat_clauses = parser.solutionStatus(instance, self.format_solution(tmp_solution))

                # if solution has been found terminate the search
                if solution_status:
                    print("Solution found at iteration: {0}, during {1} restart.\nSolution is: {2}".format(iteration, restart, tmp_solution))
                    return

                # if solution hasn't been found check if proposed temp solution is better than previous best
                if no_of_unsat_clauses < best_no_of_unsat_clauses:
                    best_no_of_unsat_clauses = no_of_unsat_clauses
                    currently_best_solution = tmp_solution
                    print("Current best no of unsat {0}, proposed best no of unsat {1}, tmp solution {2}, currently best solution {3}". format(best_no_of_unsat_clauses, no_of_unsat_clauses,tmp_solution, currently_best_solution))

            best_solution = currently_best_solution
            print("############ restart #################")


    def simple_solution(self, instance_path):
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
            self.flip_variable(variables)
            formattedSol = self.format_solution(variables)
            status = parser.solutionStatus(instance, formattedSol)
            iter_count = iter_count + 1
        print("Solution found after {0} iterations. \n Solution is: {1}".format(iter_count, formattedSol))

    def flip_variable(self, variables):
        #print("vars before flip: ", variables)
        maxVar = len(variables) - 1

        positionOfVarToFlip = rd.randint(0, maxVar)
        varToFlip = variables[positionOfVarToFlip]

        if varToFlip == 0:
            variables[positionOfVarToFlip] = 1
        else:
            variables[positionOfVarToFlip] = 0

        return variables

    def initialize_variables(self, count):
        return np.random.randint(2, size=count)

    def format_solution(self, solution_proposed):
        tmp = {}
        for var in range(0, len(solution_proposed)):
            tmp[var + 1] = solution_proposed[var]

        # printIfDebugOn("Formatted solution {0}". format(tmp), debug)
        return tmp


if __name__ == '__main__':
    solver = GsatSolver()

    if len(sys.argv) > 1:
        solver.main(10, 1000, sys.argv[1])
    else:
        solver.main()
