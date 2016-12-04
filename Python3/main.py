import sys, time

from argparse import ArgumentParser
from copy import deepcopy
from functions import Board, CSP
from functions import create_board, get_least_conflicts_y, min_conflicts, print_board
from random import choice

parser = ArgumentParser(description="A N-Queens Solver")
parser.add_argument('n', type=int, help="The number of queens")
parser.add_argument('-v', action='store_true', dest='verbose')
args = parser.parse_args()

n = args.n

start_time = time.time()

board = Board(n)
variables = [i for i in range(1, n+1)]
_var = deepcopy(variables)
constraints = {i: 0 for i in variables}

y = choice(_var)
domains = {1: y}
_var.remove(y)
board.set_queen(1, y, constraints)

for i in range(2, n+1):
    y = get_least_conflicts_y(i, n, domains, _var, board)
    domains[i] = y
    board.set_queen(i, y, constraints)
    _var.remove(y)

csp = CSP(variables, domains, constraints)

print('Set-up Time: {:0.5f} secs'.format(time.time() - start_time))
# UNCOMMENT TO SEE BOARD
# print('Initial')
# b = create_board(n)
# for key, value in csp.domains.items():
#     b[value - 1][key - 1] = 'Q'
# print_board(b)
# print()

# max_steps defaults at 100
assignment = min_conflicts(csp, n, board) #, max_steps=500)

if assignment:
    print('Time: {:0.5f} secs'.format(time.time() - start_time))
    if (n <= 15 or args.verbose):
        print()
        print('Complete')
        b = create_board(n)
        for key, value in assignment.domains.items():
            b[value - 1][key - 1] = 'Q'
            print_board(b)
    else:
        f = open("output.txt", 'w')
        print(csp.domains, file=f)
        f.close()

else:
    print('Increase Max Steps to solve.')
