# Getting all experiments in a single command
A master experiment file running the following experiments has been constructed.
- 100 GSAT experiments with `uf20-020.cnf` and `uf20-021.cnf` each
- 100 Novelty+ experiments with `uf20-020.cnf` and `uf20-021.cnf` each
- 5 TSP experiments with nearest neighbour 
- 5 TSP experiments with random tour

Master file can be executed as follows:
`python master_experiment_coordinator.py > results_file.csv`

It is all setup to run 100 experiments for GSAT/Novelty+ and 5 for each TSP algorithm, for each input file and all data has been hardcoded for ease of running.

It has been setup to collect all print statements, with
 - 1 print line for each solution found for GSAT/Novelty+ 
 - for each TSP experiment it will record
    - an initial cost
    - algorithm used (nn or rt)
    - if time limit was exceeded while executing local search
    - final cost identified per iteration
    - overall improvement over the initial solution
 into a single file with console redirect as per command above. 

If file redirect is omitted all results will be printed to the console.

# How to identify a solution?
For each of the algorithms implemented, if a solution has been identified a single print statement will be shown in the console in the following format:
 - __GSAT:__ ___Iteration,1,Restart,0,Duration,12.8___- specifying during which restart and iteration a solution has been found, as well as how long it took in seconds, to find it
 - __Novelty and Novelty+:__ ___Iteration,48020,Duration,18.190040349960327___- since as per project specification, no restarts were allowed for these algorithms a solution print only provides information about which iteration has it been found and how long it took to find it in seconds
 - __TSP:__ ___Final cost, 16202449.442113629, Improvement, 1383609.2109399643___ - will be displayed at the end of each improvement search iteration. There is no final solution for TSP, as opposed to GSAT/Novelty+ problems, as the objective here is to minimize the cost function, represented by the distance. 

 
# Project structure
This project contains the following source files and folders:
- __master_experiment_coordinator.py__ - used to gather all experiment data in 1 go
- __Algorithm Files__
    - gsat_solver.py - GSAT implementation
    - novelty_plus_solver.py - Novelty+ implementation
    - walk_sat.py - WalkSAT implementation, used as part of Novelty+ execution
    - novelty_search.py - Novelty implementation, used as part of Novelty+ execution 
    - tsp_solver.py - TSP implementation with both nearest neighbours and random tours algorithms
- __Utilities files__
    - sat_utils.py - holds various core functions, e.g. initializing variables, flipping variable values, etc
- __Data Folders__
    - sat_data - holds CNF data for experiments
    - sat_test_data - holds CNF file used in unit tests
    - tsp_data - holds TSP distance files
- __test_solvers_and_utils.py__ - contains unit tests for various core functions 

# Running individual algorithms
Additionally to running all experiments in 1 command, each algorithm, except WalkSAT, has been setup to be run in isolation. 
As a result you could run GSAT, Novelty or Novelty+ individually, with either a specific CNF input file path provided or with a default one.

## Running GSAT
To run GSAT in isolation there are 2 varieties of the commands to use:

`python gsat_solver.py`
will run the algorithm with the default CNF input file ___uf20-020.cnf___

or
 
`python gsat_solver.py <path_to_cnf_file>` will run it with CNF file specified 

## Running Novelty
To run Novelty in isolation there are 2 varieties of the commands to use:

`python novelty_search.py` will run the algorithm with the default CNF input file ___uf20-020.cnf___

or 

`python novelty_search.py <path_to_cnf_file>` will run it with CNF file specified

## Running Novelty+
To run Novelty+ in isolation there are 2 varieties of the commands to use:

`python novelty_plus_solver.py` will run the algorithm with the default CNF input file ___uf20-020.cnf___

or 


`python novelty_plus_solver.py <path_to_cnf_file>` will run it with CNF file specified

## Runing TSP
To run TSP in isolation there are 2 varieties of the commands to use:

`python tsp_solver.py` will run the algorithm with the default TSP input file ___inst-0.tsp___

or

`python tsp_solver.py <path_to_tsp_file>` will run it with TSP file specified
