import os.path

from gsat_solver import GsatSolver
from novelty_plus_solver import NoveltyPlusSolver
from tsp_solver import TspSolver


class MasterExperiment:
    # SAT Configuration Parameters
    sat_experiment_data_dir = 'sat_data'
    sat_input_data_files = ['uf20-020.cnf', 'uf20-021.cnf']
    gsat_params = {"max_iterations": 1000, "max_restarts": 10}
    novelty_plus_params = {"max_iterations": 100000, "wp": 0.4, "p": 0.3}

    # TSP Configuration parameters
    tsp_experiment_data_dir = 'tsp_data'
    tsp_input_data_files = ['inst-0.tsp', 'inst-13.tsp']
    tsp_algorithms = [TspSolver.nn, TspSolver.rt]

    def main(self, sat_experiments_count, tsp_experiments_count):
        # First execute the GSAT and Novelty+ solvers
        self.execute_sat_solvers(sat_experiments_count)

        # The execute TSP Solver
        self.execute_tsp(tsp_experiments_count)

    def execute_sat_solvers(self, sat_experiments_count):
        gsat_solver = GsatSolver()
        novelty_plus_solver = NoveltyPlusSolver()
        for i in range(sat_experiments_count):
            for sat_file in self.sat_input_data_files:
                filepath = os.path.join(self.sat_experiment_data_dir, sat_file)
                print("########### GSAT {0}, File {1} ###########".format(i, sat_file))
                gsat_solver.main(self.gsat_params["max_restarts"], self.gsat_params["max_iterations"], filepath)
                print("########### Novelty Plus {0}, File {1} ###########".format(i, sat_file))
                novelty_plus_solver.main(self.novelty_plus_params["wp"], self.novelty_plus_params["p"],
                                         self.novelty_plus_params["max_iterations"], filepath)

    def execute_tsp(self, experiment_count):
        for i in range(experiment_count):
            for tsp_file in self.tsp_input_data_files:
                filepath = os.path.join(self.tsp_experiment_data_dir, tsp_file)

                for alg in self.tsp_algorithms:
                    print('########### TSP Experiment {0} with {1} ###########'.format(i, alg))

                    # setting up the max iterations, algorithm to be used and time limit (in seconds)
                    tsp = TspSolver(filepath, max_iterations=5, local_search_time_limit=300, algorithm=alg)

                    tsp.execute_search()


if __name__ == '__main__':
    runner = MasterExperiment()

    runner.main(100, 5)
