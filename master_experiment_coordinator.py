import os.path

from gsat_solver import GsatSolver
from novelty_plus import NoveltyPlus


class MasterExperiment:
    experiment_data_dir = 'sat_data'
    gsat_params = {"max_iterations": 1000, "max_restarts": 10}
    novelty_plus_params = {"max_iterations": 100000, "wp": 0.4, "p": 0.3}
    input_data_files = ['uf20-020.cnf', 'uf20-021.cnf']

    def main(self, experiments_count):
        gsat_solver = GsatSolver()
        novelty_plus_solver = NoveltyPlus()
        for i in range(experiments_count):
            for file in self.input_data_files:
                filepath = os.path.join(self.experiment_data_dir, file)
                print("########### GSAT {0} ###########".format(filepath))
                gsat_solver.main(self.gsat_params["max_restarts"], self.gsat_params["max_iterations"], filepath)
                print("########### Novelty Plus {0} ###########".format(filepath))
                novelty_plus_solver.main(self.novelty_plus_params["wp"], self.novelty_plus_params["p"], self.novelty_plus_params["max_iterations"], filepath)
        pass


if __name__ == '__main__':
    runner = MasterExperiment()

    runner.main(1)
