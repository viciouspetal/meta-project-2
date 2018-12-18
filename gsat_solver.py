import random as rd
import sys

import numpy as np

from ParseInstance import ParseInstance


class GsatSolver:
    tabu=[]
    max_tabu_elements = 5

    def main(self, max_restarts=10, max_iterations=1000, tabu_limit=5, instance_path="./sat_data/test.cnf"):
        # self.simple_solution(instance_path)
        parser = ParseInstance()
        instance = parser.readInstance(instance_path)
        var_count = len(instance[0])
        best_solution = self.initialize_variables(var_count)
        print("initial best solution: {0}".format(best_solution))

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
                self.randomly_flip_variable(tmp_solution)
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
            GsatSolver.tabu = []


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
            self.randomly_flip_variable(variables)
            formattedSol = self.format_solution(variables)
            status = parser.solutionStatus(instance, formattedSol)
            iter_count = iter_count + 1
        print("Solution found after {0} iterations. \n Solution is: {1}".format(iter_count, formattedSol))

    def randomly_flip_variable(self, variables):
        #print("vars before flip: ", variables)
        maxVar = len(variables) - 1

        position_of_var_to_flip = self.get_flip_position(maxVar)
        var_to_flip = variables[position_of_var_to_flip]

        while(self.is_var_tabu(position_of_var_to_flip)):
            position_of_var_to_flip=self.get_flip_position(maxVar)
            #print("position of var to be flipped {0}".format(position_of_var_to_flip))
            var_to_flip = variables[position_of_var_to_flip]

        self.add_to_tabu(position_of_var_to_flip)

        if var_to_flip == 0:
            variables[position_of_var_to_flip] = 1
        else:
            variables[position_of_var_to_flip] = 0

        return variables

    def get_flip_position(self, maxPosition):
        return rd.randint(0, maxPosition)

    def is_var_tabu(self, variable):
       # print("Tabu list has {0} elements. Tabu list is: {1}. Var {2} is in tabu list {3}". format(len(GsatSolver.tabu), GsatSolver.tabu, variable, variable in GsatSolver.tabu))
        return variable in GsatSolver.tabu

    def add_to_tabu(self, position_to_tabu):
        if len(GsatSolver.tabu) >= GsatSolver.max_tabu_elements:
            GsatSolver.tabu.pop(0)

        GsatSolver.tabu.append(position_to_tabu)

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
        solver.main(10, 1000, 5, sys.argv[1])
    else:
        solver.main()
