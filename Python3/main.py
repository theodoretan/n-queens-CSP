import sys
from functions import CSP, get_num_conflicts, min_conflicts
from random import randint

n = int(sys.argv[1])

# board = create_board(n)
variables = ['Q{}'.format(i) for i in range(1, n+1)]
# print(variables)

domains = {key : [int(key[1:]), randint(1, n)] for key in variables}
# print(domains)

# domains = {'Q1': [1, 2], 'Q2': [2, 4], 'Q3': [3, 1], 'Q4': [4, 3]}

# constraints = {}
constraints = {key: get_num_conflicts(domains[key], domains) for key in variables}
# print(constraints)

print()
csp = CSP(variables, domains, constraints)

assignment = min_conflicts(csp, 1000)
if not assignment:
    print(assignment)
