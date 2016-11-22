from random import randint

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

    for _, value in queens.items():
        x1, y1 = value[0], value[1]
        if (queen != value) and ((y == y1) or (y1 == pos(x, y, x1) or
            (y1 == neg(x, y, x1)))):
            count += 1
    return count


def get_conflicts(queen, queens, conflict_list=None):
    def pos(x, y, i): return i+(y-x)
    def neg(x, y, i): return -i+(y+x)
    x, y, conflicts = queen[0], queen[1], []

    if not conflict_list:
        for key, value in queens.items():
            x1, y1 = value[0], value[1]
            if (queen != value) and ((y == y1) or (y1 == pos(x, y, x1) or
                (y1 == neg(x, y, x1)))):
                conflicts.append(key)
    else:
        for key in conflict_list:
            value = queens[key]
            x1, y1 = value[0], value[1]
            if (queen != value) and ((y == y1) or (y1 == pos(x, y, x1) or
                (y1 == neg(x, y, x1)))):
                conflicts.append(key)

    return conflicts


def min_conflicts(csp, n, max_steps):
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
    for i in range(1, max_steps+1):
        conflicted = [i for i, j in csp.constraints.items() if len(j) != 0]
        if conflicted == []:
            print('Steps: {}'.format(i))
            return csp
        var = conflicted[randint(0, len(conflicted)-1)]

        value = conflicts(var, csp.domains[var], csp)
        loop = 0 # so it doesnt get stuck in an endless loop
        if past_var != []:
            if len(past_var) >= 100: past_var.pop(0)
            while (var, value) in past_var and loop < 100:
                var = conflicted[randint(0, len(conflicted)-1)]
                value = conflicts(var, csp.domains[var], csp)
                loop += 1
        if loop < 100: past_var.append((var, value))
        csp.domains[var] = [int(var[1:]), value]
        update_conflicts(csp)
    return False


def update_conflicts(csp):
    for i in csp.variables:
        csp.constraints[i] = get_conflicts(csp.domains[i], csp.domains, csp.constraints[i])
    return


def get_least_conflicts_y(x, n, assignment):
    conflict_list, min_count = [], None
    for i in range(1, n+1):
        count = get_num_conflicts([x, i], assignment)
        if min_count is not None and min_count > count:
            min_count = count
            conflict_list = [i]
        elif min_count is not None and min_count == count:
            conflict_list.append(i)
        elif min_count is None:
            min_count = count
            conflict_list = [i]

    return conflict_list[randint(0, len(conflict_list) - 1)]


def conflicts(var, v, csp):
    x, y, n = v[0], v[1], len(csp.variables)
    conflict_list, min_count = [], None

    for i in range(1, n+1):
        if i == y: continue
        count = get_num_conflicts([x, i], csp.domains)
        if min_count is not None and min_count > count:
            min_count = count
            conflict_list = [i]
        elif min_count is not None and min_count == count:
            conflict_list.append(i)
        elif min_count is None:
            min_count = count
            conflict_list = [i]

    return conflict_list[randint(0, len(conflict_list) - 1)]


def create_board(n):
    return [['-' for i in range(n)] for j in range(n)]

def print_board(board):
    for x in board:
        for y in x:
            print(y, end=' ')
        print()
    return
