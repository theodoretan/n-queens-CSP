import sys, time

from argparse import ArgumentParser
from copy import deepcopy
from functions import Board, Colours, CSP
from functions import create_board, get_least_conflicts_y, min_conflicts, print_board
from random import choice

# Argument parser for command line arguments
parser = ArgumentParser(description="A N-Queens Solver")
parser.add_argument('n', type=int, help="The number of queens")
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help="Show the solved board")
parser.add_argument('-a', '--all', action='store_true', dest='initial_board', help="Show the initial board & solved board")
args = parser.parse_args()

# the number of queens
n = args.n

start_time = time.time()

# create the board object that keeps track of the queen placements and conflicts
board = Board(n)
# variables and _vars are a list of x and y values basically
variables = [i for i in range(1, n+1)]
_var = deepcopy(variables)
# initialize the python dict of the number of conflicts for each queen
constraints = {i: 0 for i in variables}

# place the initial queen on the board randomly
y = choice(_var)
# initialize the list of domains (x->y)
domains = {1: y}
_var.remove(y)
# place the queen on the board and update the number of constraints
board.set_queen(1, y, constraints)

# place the rest of the queens
for i in range(2, n+1):
    y = get_least_conflicts_y(i, n, _var, board)
    domains[i] = y
    board.set_queen(i, y, constraints)
    _var.remove(y)

# initialize the CSP
csp = CSP(variables, domains, constraints)

print('Set-up Time: {:0.5f} secs'.format(time.time() - start_time))

# print the inital board for smaller boards and if the user wants to see larger boards
if (n <= 15 or args.initial_board):
    print()
    print('Initial Board')
    b = create_board(n)
    for key, value in csp.domains.items():
        if constraints[key] > 0:
            b[value-1][key -1] = Colours.FAIL + 'Q' + Colours.ENDC
        else:
            b[value - 1][key - 1] = Colours.OKGREEN + 'Q' + Colours.ENDC
    print_board(b)
    print()

# to calculate the solve time
solve_time = time.time()

# max_steps defaults at 100
assignment = min_conflicts(csp, n, board)
# assignment = min_conflicts(csp, n, board, max_steps=500)

# if min-conflicts solved the problem
if assignment:
    # show times
    end_time = time.time()
    print('Solve Time: {:0.5f} secs'.format(end_time - solve_time))
    print('Total Time: {:0.5f} secs'.format(end_time - start_time))

    # print the board if the board is small or the user wants to see the board for larger values
    if (n <= 15 or args.verbose or args.initial_board):
        print()
        print('Solved Board')
        b = create_board(n)
        for key, value in assignment.domains.items():
            b[value - 1][key - 1] = Colours.OKGREEN + 'Q' + Colours.ENDC
        print_board(b)
    else:
        # or print to an output.txt file if we're computing larger numbers
        with open("output.txt", "w") as f:
            print(csp.domains, file=f)
else:
    # the min-conflicts algorithm failed to solve the csp in the max steps allowed
    print('Increase Max Steps to solve.')
