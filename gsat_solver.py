import random as rd
import sys

import numpy as np

from ParseInstance import ParseInstance


class GsatSolver:

    def main(self, instance_path="./sat_data/test.cnf"):
        parser = ParseInstance()
        instance = parser.readInstance(instance_path)
        # printIfDebugOn("instance {0}".format(instance), debug)
        print("instance {0}".format(instance))

        var_count = len(instance[0])
        initialVariables = self.initialize_variables(var_count)
        print(initialVariables)

        formattedSol = self.format_solution(initialVariables)
        status = parser.solutionStatus(instance, formattedSol)

        iter_count = 0

        while not status:
            self.flip_variable(initialVariables)
            formattedSol = self.format_solution(initialVariables)
            status = parser.solutionStatus(instance, formattedSol)
            iter_count = iter_count + 1

        print("Solution found after {0} iterations. \n Solution is: {1}".format(iter_count, formattedSol))

    def flip_variable(self, variables):
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
        solver.main(sys.argv[1])
    else:
        solver.main()
