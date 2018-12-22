# Getting 100 experiments for GSAT and Novelty+
In order to get 100 experiments ran for both GSAT and Novelty+, for both `uf20-020.cnf` and `uf20-021.cnf` files use 

`python master_experiment_coordinator.py > results_file.csv`

It is all setup to run 100 experiments for each file and all data has been hardcoded for ease of running.

It has been setup to collect all print statements, with 1 print line for each solution found, into a single file with console redirect as per command above. 

If file redirect is omitted all results will be printed to the console.

# How to identify a solution?
For each of the algorithms implemented, if a solution has been identified a single print statement will be shown in the console in the following format:
 - __GSAT:____"Iteration,1,Restart,0,Duration,0.0"__- specifying during which restart and iteration a solution has been found, as well as how long it took in seconds, to find it
 - __Novelty and Novelty+:____"Iteration,48020,Duration,18.190040349960327"__- since as per project specification, no restarts were allowed for these algorithms a solution print only provides information about which iteration has it been found and how long it took to find it in seconds
 
# Project structure
This project contains the following source files and folders:
- __master_experiment_coordinator.py__ - used to gather all experiment data in 1 go
- __Algorithm Files__
    - gsat_solver.py - GSAT implementation
    - novelty_plus.py - Novelty+ implementation
    - walk_sat.py - WalkSAT implementation, used as part of Novelty+ execution
    - noveltysearch.py - Novelty implementation, used as part of Novelty+ execution 
- __Utilities files__
    - SatUtils.py - holds various core functions, e.g. initializing variables, flipping variable values, etc
- __Data Folders__
    - sat_data - holds CNF data for experiments
    - sat_test_data - holds CNF file used in unit tests
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

`python noveltysearch.py` will run the algorithm with the default CNF input file ___uf20-020.cnf___

or 

`python noveltysearch.py <path_to_cnf_file>` will run it with CNF file specified

## Running Novelty+
To run Novelty+ in isolation there are 2 varieties of the commands to use:

`python novelty_plus.py` will run the algorithm with the default CNF input file ___uf20-020.cnf___

or 


`python novelty_plus.py <path_to_cnf_file>` will run it with CNF file specified

