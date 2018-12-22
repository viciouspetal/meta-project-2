# Getting 100 experiments for GSAT and Novelty+
In order to get 100 experiments ran for both GSAT and Novelty+, for both `uf20-020.cnf` and `uf20-021.cnf` files use 

`python master_experiment_coordinator.py > results_file.csv`

It is all setup to run 100 experiments for each file and all data has been hardcoded for ease of running.

It has been setup to collect all print statements, with 1 print line for each solution found, into a single file with console redirect as per command above. 

If file redirect is omitted all results will be printed to the console.

# How to identify a solution?
For each of the algorithms implemented, if a solution has been identified a single print statement will be shown in the console in the following format:
 - __GSAT:__ __"Iteration,1,Restart,0,Duration,0.0"__ - specifying during which restart and iteration a solution has been found, as well as how long it took in seconds, to find it
 - __Novelty & Novelty+:__ __"Iteration,48020,Duration,18.190040349960327"__ - since no restarts were specified for these algorithms, a solution print only provides information about which iteration has it been found and how long it took to find it in seconds 

# Running individual algorithms
Additionally to running all experiments in 1 command, each algorithm, except WalkSAT has been setup to be run in isolation. As a result you could run GSAT, Novelty or Novelty+ individually.
## Running GSAT
`python gsat_solver.py`

## Running Novelty
`python noveltysearch.py`

## Running Novelty+
`python novelty_plus.py`

