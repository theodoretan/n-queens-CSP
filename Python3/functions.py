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

    for i in range(1, max_steps+1):
        # print(csp.domains)
        # print(csp.constraints)
        conflicted = [i for i, j in csp.constraints.items() if len(j) != 0]
        if conflicted == []:
            print(i)
            return csp
        # print(get_min_conflicts(conflicted, csp))
        var = conflicted[randint(0, len(conflicted)-1)]

        # var = get_min_conflicts(conflicted, csp)
        value, count= conflicts(var, csp)
        if past_var != []:
            if len(past_var) >= 100: past_var.pop(0)
            while (var, value) in past_var:
                var = conflicted[randint(0, len(conflicted)-1)]
                value, count = conflicts(var, csp)
        past_var.append((var, value))
        csp.domains[var] = [int(var[1:]), value]
        # if count > 0:
        update_conflicts(csp)
        # else:
        #     csp.constraints[var] = count
    return False


def update_conflicts(csp):
    for i in csp.variables:
        csp.constraints[i] = get_conflicts(csp.domains[i], csp.domains, csp.constraints[i])
    return


def get_min_conflicts(conflicted, csp):
    least = conflicted[0]
    for x in conflicted:
        if len(csp.constraints[least]) > len(csp.constraints[x]):
            least = x
    return least


def conflicts(var, csp):
    column, asdf = {}, []
    x = int(var[1:])
    min_column = 1 if 1 != csp.domains[var][1] else 2
    min_count = len(get_conflicts([x, min_column], csp.domains))
    for y in range(1, len(csp.variables)+1):
        if y != csp.domains[var][1]:
            count = len(get_conflicts([x, y], csp.domains))
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

    # print(min_count)
    return min_column, min_count


def create_board(n):
    return [['-' for i in range(n)] for j in range(n)]

def print_board(board):
    for x in board:
        for y in x:
            print(y, end=' ')
        print()
    return
