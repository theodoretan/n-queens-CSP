from random import randint
import time

class CSP():
    """
    ------------------------------------------------------
    A CSP object that holds the variables, domains and
    constraints
    ------------------------------------------------------
    """
    def __init__(self, variables , domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints


def get_num_conflicts(queen, queens):
    """
    ------------------------------------------------------
    Get number of conflicts for that square
    ------------------------------------------------------
    Inputs:
        queen - [x, y] (list)
        queens - csp.domains (key-pair list)
    Returns:
        count - number of conflicts for the square
    ------------------------------------------------------
    """
    def pos(x, y, i): return i+(y-x)
    def neg(x, y, i): return -i+(y+x)
    x, y, count = queen[0], queen[1], 0

    for q in queens:
        x1, y1 = queens[q][0], queens[q][1]
        if (queen != queens[q]) and ((y == y1) or (y1 == pos(x, y, x1) or
            (y1 == neg(x, y, x1)))):
            count += 1
    return count


def min_conflicts(csp, max_steps):
    """
    ------------------------------------------------------
    Min-Conflicts algorithm for solving CSPs by
    local search
    ------------------------------------------------------
    Inputs:
        csp - a CSP with components(X, D, C)
        max_steps - the number of steps allowed before
            giving up
    Returns:
        A solution or failure (False)
    ------------------------------------------------------
    """
    # current = initial complete assignment for csp
    # pass in csp as a complete inital assignment
    past_var = []
    start_time = time.time()
    for i in range(1, max_steps+1):
        # print(csp.domains)
        # print(csp.constraints)
        conflicted = [i for i in csp.variables if csp.constraints[i] != 0]
        if not any(conflicted):
            print(i)
            end = (time.time() - start_time)
            print("{}".format(end))
            return csp
        # print(get_min_conflicts(conflicted, csp))
        var = conflicted[randint(0, len(conflicted)-1)]

        # var = get_min_conflicts(conflicted, csp)
        value= conflicts(var, csp)
        if past_var is not []:
            if len(past_var) >= 50: past_var.pop(0)
            while (var, value) in past_var:
                var = conflicted[randint(0, len(conflicted)-1)]
                value = conflicts(var, csp)
        else: past_var.append((var, value))
        csp.domains[var] = [int(var[1:]), value]
        update_conflicts(csp)
        #csp.constraints[var] = count
    end = (time.time() - start_time)
    print("{}".format(end))
    return False


def update_conflicts(csp):
    for i in csp.variables:
        csp.constraints[i] = get_num_conflicts(csp.domains[i], csp.domains)
    return


def get_min_conflicts(conflicted, csp):
    least = conflicted[0]
    for x in conflicted:
        if csp.constraints[least] > csp.constraints[x]:
            least = x
    return least


def conflicts(var, csp):
    column, asdf = {}, []
    x = int(var[1:])
    min_column = 1 if 1 != csp.domains[var][1] else 2
    min_count = get_num_conflicts([x, min_column], csp.domains)
    for y in range(1, len(csp.variables)+1):
        if y != csp.domains[var][1]:
            count = get_num_conflicts([x, y], csp.domains)
            if count < min_count:
                column = {}
                column[y] = count
                asdf = [y]
                min_count = count
                min_column = y
            elif count <= min_count:
                column[y] = count
                asdf.append(y)
    if len(asdf) > 1:
        rand = randint(0, len(asdf)-1)
        min_count = column[asdf[rand]]
        min_column = asdf[rand]

    return min_column



def create_board(n):
    return [['-' for i in range(n)] for j in range(n)]

def print_board(board):
    for x in board:
        for y in x:
            print(y, end=' ')
        print()
    return
