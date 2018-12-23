from reader import Reader
import re
import numpy as np


class ResultsParser:
    gsat_iterations = {}
    gsat_restarts = {}
    gsat_durations = {}

    novelty_iterations = {}
    novelty_durations = {}

    def main(self):
        gsat_sep = re.compile('.*GSAT.*\d?.*File.*')
        novelty_sep = re.compile('.*Novelty.*Plus\d?.*File.*')
        gsat_solution_pattern = re.compile('Iteration,\d+,Restart,\d,Duration,\d+.\d*.*')
        novelty_solution_pattern = re.compile('Iteration,\d+,Duration,\d+.\d*.*')

        reader = Reader('./data.csv')
        lines = reader.read()
        file_020 = 'uf20-020.cnf'
        file_021 = 'uf20-021.cnf'
        file_020_pattern = re.compile('.*uf20-020.cnf.*')
        file_021_pattern = re.compile('.*uf20-021.cnf.*')

        file_20_gsat_lines = 0
        file_20_gsat_sol_found = 0
        file_20_novelty_lines = 0
        file_20_novelty_sol_found = 0

        file_21_gsat_lines = 0
        file_21_gsat_sol_found = 0
        file_21_novelty_lines = 0
        file_21_novelty_sol_found = 0

        for i in range(0, len(lines)):
            if gsat_sep.match(lines[i]) and file_020_pattern.match(lines[i]):
                file_20_gsat_lines += 1
            elif gsat_solution_pattern.match(lines[i]) and file_020_pattern.match(lines[i - 1]):
                file_20_gsat_sol_found += 1
                self.split_gsat_line_into_tokens(lines[i], file_020)
            if novelty_sep.match(lines[i]) and file_020_pattern.match(lines[i]):
                file_20_novelty_lines += 1
            if novelty_solution_pattern.match(lines[i]) and file_020_pattern.match(lines[i - 1]):
                file_20_novelty_sol_found += 1
                self.split_novelty_line_into_tokens(lines[i], file_020)

            if gsat_sep.match(lines[i]) and file_021_pattern.match(lines[i]):
                file_21_gsat_lines += 1
            elif gsat_solution_pattern.match(lines[i]) and file_021_pattern.match(lines[i - 1]):
                file_21_gsat_sol_found += 1
                self.split_gsat_line_into_tokens(lines[i], file_021)
            elif novelty_sep.match(lines[i]) and file_021_pattern.match(lines[i]):
                file_21_novelty_lines += 1
            elif novelty_solution_pattern.match(lines[i]) and file_021_pattern.match(lines[i - 1]):
                file_21_novelty_sol_found += 1
                self.split_novelty_line_into_tokens(lines[i], file_021)

        self.print_results_per_file(file_020, file_20_gsat_lines, file_20_gsat_sol_found, file_20_novelty_lines,
                                    file_20_novelty_sol_found, len(lines))
        self.print_results_per_file(file_021, file_21_gsat_lines, file_21_gsat_sol_found, file_21_novelty_lines,
                                    file_21_novelty_sol_found, len(lines))

    def print_results_per_file(self, filename, gsat_lines, gsat_sol_found, novelty_lines, novelty_sol_found,
                               line_count):

        gsat_sol_per = gsat_sol_found / gsat_lines * 100
        novelty_sol_per = novelty_sol_found / novelty_lines * 100

        print('Results for file {0}'.format(filename))
        print('GSAT')
        print('________________________________________________________________________________________')
        print('GSAT Experiments run {0}, solutions found {1}, acc {2}%'.format(gsat_lines, gsat_sol_found, gsat_sol_per))
        print('Iterations Average, {0}, Iterations Min, {1}, Iterations Max, {2}, Iterations Median, {3}'.format(np.average(
            self.gsat_iterations.get(filename)), np.min(self.gsat_iterations.get(filename)), np.max(self.gsat_iterations.get(filename)), np.median(self.gsat_iterations.get(filename))))
        print('Duration Average, {0}, Duration Min, {1}, Duration Max, {2}, Duration Median, {3}'.format(np.average(
            self.gsat_durations.get(filename)), np.min(self.gsat_durations.get(filename)), np.max(self.gsat_durations.get(filename)), np.median(self.gsat_durations.get(filename))))
        print('Restarts Average, {0}, Restarts Min, {1}, Restarts Max, {2}, Restarts Median, {3}'.format(np.average(
            self.gsat_restarts.get(filename)), np.min(self.gsat_restarts.get(filename)), np.max(self.gsat_restarts.get(filename)), np.median(self.gsat_restarts.get(filename))))

        print()
        print('Novelty+')
        print('________________________________________________________________________________________')
        print('Novelty+ Experiments run {0}, solutions found {1}, acc {2}%'.format(novelty_lines, novelty_sol_found,
                                                                           novelty_sol_per))
        print('Iterations Average, {0}, Iterations Min, {1}, Iterations Max, {2}, Iterations Median, {3}'.format(np.average(
            self.novelty_iterations.get(filename)), np.min(self.novelty_iterations.get(filename)), np.max(self.novelty_iterations.get(filename)), np.median(self.novelty_iterations.get(filename))))
        print('Duration Average, {0}, Duration Min, {1}, Duration Max, {2}, Duration Median, {3}'.format(np.average(
            self.novelty_durations.get(filename)), np.min(self.novelty_durations.get(filename)), np.max(self.novelty_durations.get(filename)), np.median(self.novelty_durations.get(filename))))
        print('####################################################################################################################')

    def split_gsat_line_into_tokens(self, line, file_ind):
        tokens = line.split(',')

        if self.gsat_iterations.get(file_ind) is None:
            current_iterations = []
        else:
            current_iterations = self.gsat_iterations.get(file_ind)
        current_iterations.append(int(tokens[1]))

        if self.gsat_restarts.get(file_ind) is None:
            current_restarts = []
        else:
            current_restarts = self.gsat_restarts.get(file_ind)
        current_restarts.append(int(tokens[3]))

        if self.gsat_durations.get(file_ind) is None:
            current_durations = []
        else:
            current_durations = self.gsat_durations.get(file_ind)
        current_durations.append(float(tokens[5].replace('\n', '')))

        self.gsat_iterations[file_ind] = current_iterations
        self.gsat_restarts[file_ind] = current_restarts
        self.gsat_durations[file_ind] = current_durations

    def split_novelty_line_into_tokens(self, line, file_ind):
        tokens = line.split(',')
        if self.novelty_iterations.get(file_ind) is None:
            current_iterations = []
        else:
            current_iterations = self.novelty_iterations.get(file_ind)

        if self.novelty_durations.get(file_ind) is None:
            current_durations = []
        else:
            current_durations = self.novelty_durations.get(file_ind)

        current_iterations.append(int(tokens[1]))
        current_durations.append(float(tokens[3].replace('\n', '')))
        self.novelty_iterations[file_ind] = current_iterations
        self.novelty_durations[file_ind] = current_durations


if __name__ == '__main__':
    parser = ResultsParser()

    parser.main()
