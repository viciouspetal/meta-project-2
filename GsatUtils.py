
import sys

import numpy as np

class GsatUtils:

    def read_instance(self, fName):
        """Based off of Week 8 Lab
        Reads in a a CNF file from a path provided.
        Returns an array of arrays, where element 0 contains variables, and element 1 in itself is an array of arrays
        where each internal array represents a 3-variable clause to be fulfilled.
        :param fName: relative path to cnf file to be read in
        :return variables and the formula
        """
        file = open(fName, 'r')
        tVariables = -1
        tClauses = -1
        clause = []
        variables = []

        current_clause = []

        for line in file:
            data = line.split()

            if len(data) == 0:
                continue
            if data[0] == 'c':
                continue
            if data[0] == 'p':
                tVariables = int(data[2])
                tClauses = int(data[3])
                continue
            if data[0] == '%':
                break
            if tVariables == -1 or tClauses == -1:
                print("Error, unexpected data")
                sys.exit(0)

            ## now data represents a clause
            for var_i in data:
                literal = int(var_i)
                if literal == 0:
                    clause.append(current_clause)
                    current_clause = []
                    continue
                var = literal
                if var < 0:
                    var = -var
                if var not in variables:
                    variables.append(var)
                current_clause.append(literal)

        if tVariables != len(variables):
            print("Unexpected number of variables in the problem")
            print("Variables", tVariables, "len: ", len(variables))
            print(variables)
            sys.exit(0)
        if tClauses != len(clause):
            print("Unexpected number of clauses in the problem")
            sys.exit(0)
        file.close()
        return [variables, clause]

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

    def initialize_variables(self, count):
        """
        Initialize a dictionary of a given size - defined by count parameter - with randomly assigned 0 or 1 values.
        :param count: the number of variables to be initialized
        :return: a dictionary initialized with randomly assigned 0 and 1 values
        """

        return dict(enumerate(np.random.randint(2, size=count), 1))

    def solution_status(self, formula, sol):
        """
        Based off of Week 8 Lab.

        Verifies the number of unsatisified clauses for a given solution proposed. Returns True if a solution
        satisfying all clauses has been found.
        Returns False along with the number of unsatisfied clauses if a solution has not been found.
        :param formula: the formula to be satisfied
        :param sol: proposed solution to be verified against the formula
        :return: True if solution satisfies the formula. Otherwise returns False and the number of unsatisfied clauses.
        """
        clause = formula[1]
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
            return False, unsat_clause
        return True, unsat_clause