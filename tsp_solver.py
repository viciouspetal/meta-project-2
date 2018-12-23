import math
import random
import sys
import time


class TspSolver:
    nn = 'nearest_neighbours'
    rt = 'random_tours'

    def __init__(self, filepath, max_iterations, local_search_time_limit, algorithm):
        self.filepath = filepath
        self.instance_count = 0
        self.data = {}
        self.data_list = []
        self.max_iterations = max_iterations
        self.local_search_time_limit = local_search_time_limit
        self.algorithm = algorithm

    def read_instance(self):
        """
        Read TSP file from a given file pth
        """
        file = open(self.filepath, 'r')
        self.instance_count = int(file.readline())
        for line in file:
            (id, x, y) = line.split()
            self.data[int(id)] = (int(x), int(y))

        self.data_list = list(self.data.keys())
        file.close()

    def calc_euclidean_distance(self, c1, c2):
        """
        Calculate the Euclidean distance between two cities.
        """
        d1 = self.data[c1]
        d2 = self.data[c2]
        return math.sqrt((d1[0] - d2[0]) ** 2 + (d1[1] - d2[1]) ** 2)

    def generate_random_tour(self):
        """
        Generates a random tour, or route of specified cities where the starting point and the end point are the same.
        It is important to note that each city in the route can only be visited once - no repetitions are allowed.
        :return: a tour, comprising of the cities visited
        """
        print('Generating initial random tour')
        tour = self.data_list.copy()

        random.shuffle(tour)

        # append the starting point to the end of the list to complete the loop
        tour.append(tour[0])

        return tour

    def generate_nearest_neighbour_tour(self):
        """
        A greedy nearest neighbour algorithm implementation. It is used to generate a tour of cities to be visited
        as part of the TSP problem. Works by picking a random starting point, finding the nearest point, based on
        euclidean distance, and adding it to the list of cities visited so far and removing same from the list of cities
        to be visited as no repetitions in the tour are allowed.

        :return: a tour, comprising of the cities visited
        """
        print('Generating initial nearest neighbours')
        tour = self.data.copy()
        tour2 = tour.copy()
        random_start_point = random.choice(list(tour))
        new_tour = []
        current_location = random_start_point

        for i in tour2:
            nearest_city = None
            distance_to_nearest_city = None

            for city in tour.keys():

                distance = self.calc_euclidean_distance(current_location, city)

                # for the first iteration guard against unset variables.
                if nearest_city is None or distance < distance_to_nearest_city:
                    nearest_city = city
                    distance_to_nearest_city = distance

            new_tour.append(nearest_city)
            del tour[nearest_city]

        # appending the starting point to the end to close the route loop
        new_tour.append(new_tour[0])

        return new_tour

    def three_opt(self, potential_solution, cost):
        """
        Implements the 3-opt algorithm by swapping 3 cities in a given tour. After each swap a cost of the new tour is
        calculated. This is done to identify the route, or tour with the greatest distance reduction over the
        initial solution.

        As the process can take a long time, the longer the rout the longer it will take, it is necessary to impose
        a time limit. After the time limit has been exceeded in the local search, best route, or tour, identified so far
        is returned for further processing.
        :param potential_solution: the current best route (or tour)
        :param cost: the shortest distance of the given route identified so far
        :return: the new shortest route along with its cost (distance)
        """
        # initializing the temporary solution that will have its rout sliced and swapped and
        tmp_solution = potential_solution.copy()

        new_cost = cost
        start_time = time.time()
        data_to_search = self.data_list

        # executing the local search for shortest distance with swapped cities
        for city_1 in data_to_search:
            for city_2 in data_to_search:
                for city_3 in data_to_search:
                    # generate a new potential solution by switching the 3 selected cities in the tour
                    tmp_new_solution = self.generate_3_opt_swap(city_1, city_2, city_3, tmp_solution)
                    # check the cost of the new potential solution
                    tmp_new_cost = self.calculate_cost(tmp_new_solution)
                    # compare the cost. If newly generated solution shortened the tour distance then
                    if tmp_new_cost < cost:
                        potential_solution = tmp_new_solution
                        new_cost = tmp_new_cost

                    # check if the allocated time limit has ben exceeded in local search. If it has, then return the
                    # best solution found so far.
                    if (time.time() - start_time) > self.local_search_time_limit:
                        print('Local search time exceeded. Returning best solution and cost')
                        return potential_solution, new_cost

        return potential_solution, new_cost

    def generate_3_opt_swap(self, city_1, city_2, city_3, route_to_be_modified):
        """
        Swaps cities at given indices.
        :param city_1: first city to be swapped
        :param city_2: second city to be swapped
        :param city_3: third city to be swapped
        :param route_to_be_modified: route on which cities will be swapped
        :return: modified route
        """
        # adding 1 to the swapping index as slicing would have omitted the actual city to be swapped
        route_part_up_to_1_slice_point = route_to_be_modified[:city_1]
        swapping_city_1_and_2 = route_to_be_modified[city_1:city_2 + 1][::-1]
        swapping_city_2_and_3 = route_to_be_modified[city_2 + 1:city_3 + 1][::-1]
        remainder_of_the_route = route_to_be_modified[city_3 + 1:]

        return route_part_up_to_1_slice_point + swapping_city_1_and_2 + swapping_city_2_and_3 + remainder_of_the_route

    def two_opt(self, potential_solution, max_iterations):
        """
        Implements 2-opt algorithm by first choosing 2 random variables to swap and executing the swap a given number of times.
        :param potential_solution: represents the current tour as a potential solution
        :param max_iterations: number of times 2-OPT will be executed
        :return: new potential solution with swapped locations
        """
        tmp_solution = potential_solution.copy()

        for i in range(max_iterations):
            # pick random locations to be swapped in the TSP route
            random_locations = random.sample(range(len(self.data_list)), 2)

            # swap edges and return the final solution
            tmp_solution[random_locations[0]] = potential_solution[random_locations[1]]
            tmp_solution[random_locations[1]] = potential_solution[random_locations[0]]

        return tmp_solution

    def calculate_cost(self, tour):
        """
        Calculating the cost of a given tour by summing up the distances between individual points in the tour
        :param tour: the current tour
        :return: returns the calculated cost of the tour
        """
        cost = 0
        for i in range(self.instance_count - 1):
            cost += self.calc_euclidean_distance(tour[i], tour[i + 1])

        return cost

    def execute_search(self):
        """
        Main execute point - initializes the first solution based on the algorithm specified when solver was
        instantiated. Delegates to other functions for cost calculation etc. It's responsible for printing out the final
        improvements and solutions identified as best, based on distance improvement of a given route.
        """
        self.read_instance()
        initial_solution = self.data_list

        # generate the initial solution based on specified algorithm
        if self.algorithm == self.nn:
            initial_solution = self.generate_nearest_neighbour_tour()
        elif self.algorithm == self.rt:
            initial_solution = self.generate_random_tour()

        # calculate initial cost of the solution
        initial_cost = self.calculate_cost(initial_solution)

        print('Initial Cost, {0}'.format(initial_cost))

        # copy the initial solution to avoid it being changed.
        solution = initial_solution.copy()
        cost = initial_cost

        # execute the 3-OPT algorithm
        solution, cost = self.three_opt(solution, cost)

        for i in range(self.max_iterations):
            solution = self.two_opt(solution, self.max_iterations)
            solution, cost = self.three_opt(solution, cost)

        route_improvement = initial_cost - cost
        print('Final cost, {0}, Improvement, {1}'.format(cost, route_improvement))


if __name__ == '__main__':
    instance_path = None
    # check whether a path to input dataset has been provided or should the default path be used
    if len(sys.argv) > 1:
        instance_path = sys.argv[1]
    else:
        instance_path = './tsp_data/inst-0.tsp'

    solver = TspSolver(instance_path, 1, 300, TspSolver.nn)
    solver.execute_search()
