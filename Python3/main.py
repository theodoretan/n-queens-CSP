import sys, time
from argparse import ArgumentParser
from functions import CSP, get_conflicts, min_conflicts, create_board, print_board, get_least_conflicts_y, get_empty_spot
from random import randint

parser = ArgumentParser(description="A N-Queens Solver")
parser.add_argument('n', type=int, help="The number of queens")
args = parser.parse_args()

n = args.n

start_time = time.time()

variables = ['Q{}'.format(i) for i in range(1, n+1)]
# domains = {key : [int(key[1:]), randint(1, n)] for key in variables}
domains = {}
for i in range(1, n+1):
    # if (i < 200):
        domains['Q{}'.format(i)] = get_least_conflicts_y(i, n, domains)
    # else:
    #     domains['Q{}'.format(i)] = i

constraints = {key: get_conflicts([int(key[1:]), domains[key]], domains) for key in variables}

# Setup Time
print('Set-up Time: {:0.5f} secs'.format(time.time() - start_time))



csp = CSP(variables, domains, constraints)

# UNCOMMENT TO SEE BOARD
# print('Initial')
# b = create_board(n)
# for key, value in csp.domains.items():
#     b[value[1] - 1][int(key[1:]) - 1] = 'Q'
# print_board(b)
# print()

assignment = min_conflicts(csp, n, max_steps=100)

if assignment: print('Time: {:0.5f} secs'.format(time.time() - start_time))

# UNCOMMENT TO SEE BOARD
# if not assignment:
#     print(assignment)
# else:
#     print()
#     print('Complete')
#     b = create_board(n)
#     for key, value in assignment.domains.items():
#         b[value[1] - 1][int(key[1:]) - 1] = 'Q'
#     print_board(b)
