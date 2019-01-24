The python class auto_assigner in autoassigner.py implements the PeerReview4All algorithm (PR4A) of the paper "PeerReview4All: Fair and Accurate Reviewer Assignment in Peer Review" by Ivan Stelmakh, Nihar Shah and Aarti Singh.

DEPENDENCIES:
This code uses the gurobipy package in python for solving the Linear Programming problems. Gurobi offers free academic licenses for universities. To obtain your license, please go to http://www.gurobi.com/academia/for-universities and follow the instructions provided there.

INPUTS:
'simmatrix' is an n x m matrix with entries in {-1}U[0, 1], where n = number of reviewers, m = number of papers and any conflict of interest is handled by setting the corresponding entry to -1 . 'demand' is a number of reviewers required per paper and 'ability' is a maximum number of papers that reviewer can review.'function' is any monotonically increasing function (identity by default) of similarities which defines the notion of fairness. 'iter_limit' is a maximum number of iterations of Steps 2 to 7 of the algorithm ('inf' by default). 'time_limit' is a time limit in seconds ('inf' by default) -- the algorithm starts new iteration if the exceeded time is below the time limit. 

HOWTO:
The entry point of the class is the function 'fair_assignment' which takes no arguments and performs the assignment using the parameters supplied to class constructor. 

To ensure fairness guarantees, the code requires that at least one iteration of Steps 2 to 7 is performed, consequently, the actual running time of the algorithm might be larger than 'time_limit' ( at most max{2*'time_limit', time of the first iteration)} ). Notice that fairness and statistical results are guaranteed after the first iteration of Steps 2 to 7 of the algorithm, but additional iterations optimize assignment for the second worst-off paper and so on.  

COMMENT:
The current implementation takes about 90 minutes to perform a single iteration of Steps 2 to 7 for large scale assignment problem (10,000 papers and 10,000 reviewers).

OUTPUT:
A dictionary of the form {paper: [assigned_reviewers]} that encodes the resulting assignment.

EXAMPLE:
A minimum working example is constructed in working_example.ipynb