import numpy as np
from ParseInstance import ParseInstance
import sys


class GsatSolver:

    def main(self, instance_path="./sat_data/test.cnf"):
        parser = ParseInstance()
        instance = parser.readInstance(instance_path)
        #print("instance {0}".format(instance))

        var_count = len(instance[0])
        initialVariables = self.initializeVariables(var_count)
        print(initialVariables)

        formattedSol = self.formatSolution(initialVariables)
        parser.solutionStatus(instance, formattedSol)

    def initializeVariables(self, count):
        return np.random.randint(2, size=count)

    def formatSolution(self, solutionProposed):
        # format {ordinalOfVariable: variableValue, ordinalOfVariable: variableValue}
        tmp = {}
        for var in range(0, len(solutionProposed)):
            tmp[var+1] = solutionProposed[var]

        print("Formatted solution {0}". format(tmp))
        return tmp


if __name__ == '__main__':
    solver = GsatSolver()
    path = sys.argv[1]
    if(path != None):
        solver.main(path)
    else:
        solver.main()
