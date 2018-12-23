import random

from sat_utils import SatUtils


class WalkSat:

    def execute_walk(self, formula, proposed_solution):
        solution_found, unsat_clause, unsat_clause_list = SatUtils.solution_status_with_unsat_clauses(formula,
                                                                                                      proposed_solution)

        random_unsat_clause = random.choice(unsat_clause_list)

        random_variable_in_clause = random.choice(random_unsat_clause)

        # as we're choosing a variable from the unsat clause we can come across negative numbers, where negative
        # sign would indicate variable is in 0 state, however, negative index are not present in the proposed solution
        # array, so it needs to be guaranteed that a positive number is passed as index, hence use of abs()
        proposed_solution[abs(random_variable_in_clause)] = SatUtils.flip_var(abs(random_variable_in_clause))

        return proposed_solution
