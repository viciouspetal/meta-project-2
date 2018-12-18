"""Based off of Week 8 Lab"""
import sys


class ParseInstance:

    def readInstance(self, fName):
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