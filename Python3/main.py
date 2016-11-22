import sys, time
from functions import CSP, get_conflicts, min_conflicts, create_board, print_board, get_least_conflicts_y
from random import randint

n = int(sys.argv[1])

start_time = time.time()

variables = ['Q{}'.format(i) for i in range(1, n+1)]
# domains = {key : [int(key[1:]), randint(1, n)] for key in variables}
domains = {}
for i in range(1, n+1):
    domains['Q{}'.format(i)] = [i, get_least_conflicts_y(i, n, domains)]

constraints = {key: get_conflicts(domains[key], domains) for key in variables}

csp = CSP(variables, domains, constraints)

# UNCOMMENT TO SEE BOARD
# print('Initial')
# b = create_board(n)
# for key, value in csp.domains.items():
#     b[value[1] - 1][value[0] - 1] = 'Q'
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
#         b[value[1] - 1][value[0] - 1] = 'Q'
#     print_board(b)
