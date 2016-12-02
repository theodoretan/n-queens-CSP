import sys, time
from argparse import ArgumentParser
from copy import deepcopy
from functions import CSP, get_conflicts, min_conflicts, create_board, print_board, get_least_conflicts_y
from random import choice, randint

parser = ArgumentParser(description="A N-Queens Solver")
parser.add_argument('n', type=int, help="The number of queens")
args = parser.parse_args()

n = args.n

start_time = time.time()

variables = [i for i in range(1, n+1)]
_var = deepcopy(variables)
# domains = {key : [int(key[1:]), randint(1, n)] for key in variables}
domains = {}
for i in range(1, n+1):
    if i % (n//4) != 0:
        y = get_least_conflicts_y(i, n, domains, _var)
    else:
        y = choice(_var)
    domains[i] = y
    _var.remove(y)

constraints = {key: get_conflicts([key, domains[key]], domains) for key in variables}

# print([i for i, j in constraints.items() if len(j) != 0])
# input()

csp = CSP(variables, domains, constraints)

print('Set-up Time: {:0.5f} secs'.format(time.time() - start_time))
# UNCOMMENT TO SEE BOARD
# print('Initial')
# b = create_board(n)
# for key, value in csp.domains.items():
#     b[value - 1][key - 1] = 'Q'
# print_board(b)
# print()

assignment = min_conflicts(csp, n, max_steps=200)

if assignment: print('Time: {:0.5f} secs'.format(time.time() - start_time))

# UNCOMMENT TO SEE BOARD
# if not assignment:
#     print(assignment)
# else:
#     print()
#     print('Complete')
#     b = create_board(n)
#     for key, value in assignment.domains.items():
#         b[value - 1][key - 1] = 'Q'
#     print_board(b)
