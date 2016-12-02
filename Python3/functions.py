from random import choice, randint

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

# helper functions
def pos(x, y, i): return i+(y-x)
def neg(x, y, i): return -i+(y+x)

def get_num_conflicts(queen, queens):
    """
    ------------------------------------------------------
    Get number of conflicts for that square
    ------------------------------------------------------
    Inputs:
        queen - [x, y] (list)
        queens - csp.domains (key-pair list) {#: #}
    Returns:
        count - number of conflicts for the square
    ------------------------------------------------------
    """
    x, y, count = queen[0], queen[1], 0

    for key, value in queens.items():
        # get the x and y value of the queen
        x1, y1 = key, value
        # if it's not the same queen and if the value (queen) is in a position of conflict
        # it checks the y value, positive slope, and negatvie slope
        if (queen != [x1, y1]) and ((y == y1) or (y1 == pos(x, y, x1) or
            (y1 == neg(x, y, x1)))):
            count += 1
    return count


def get_conflicts(queen, queens, conflict_list=None):
    """
    ------------------------------------------------------
    Get the conflicts for that square
    ------------------------------------------------------
    Inputs:
        queen - [x, y] (list)
        queens - csp.domains (key-pair list)
        conflict_list - list of the current conflicts (list)
    Returns:
        conflicts - the conflicts for the square
    ------------------------------------------------------
    """
    x, y, conflicts = queen[0], queen[1], []

    # we're giving this fuction conflict list to reduce the search space
    if not conflict_list:
        for key, value in queens.items():
            # check if the queens aren't the same and if its in a position of conflict
            # add it to the list of conflicted queens
            x1, y1 = key, value
            if (queen != [x1, y1]) and ((y == y1) or (y1 == pos(x, y, x1) or
                (y1 == neg(x, y, x1)))):
                conflicts.append(key)
    else:
        # this just reduced the search space and does the same thing as above
        for key in conflict_list:
            # value = queens[key]
            x1, y1 = key, queens[key] #value
            if (queen != [x1, y1]) and ((y == y1) or (y1 == pos(x, y, x1) or
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
    past_var = {} # TABU SEARCH LIST
    x = 50 if n >= 100 else (n//2)
    for i in range(1, max_steps+1):
        # get the list of conflcited queens from the csp constraints
        # NOTE: constraints is the list of conflicted queens
        conflicted = [i for i, j in csp.constraints.items() if len(j) != 0]
        # if there are not more conflicting queens then the problem is sovled
        if conflicted == []:
            print('Steps: {}'.format(i))
            return csp
        # get a random queen from the conflicted list
        var = choice(conflicted)
        if var in past_var:
            if csp.domains[var] not in past_var[var]:
                past_var[var].append(csp.domains[var])
        else:
            past_var[var] = [csp.domains[var]]

        value = conflicts(var, csp.domains[var], n, csp, past_var[var])

        if len(past_var[var]) >= x: past_var[var].pop(0)

        csp.domains[var] = value
        update_conflicts(csp)
    return False


def update_conflicts(csp):
    # update the conflicts for the entire board
    for i in csp.variables:
        csp.constraints[i] = get_conflicts([i, csp.domains[i]], csp.domains)#, csp.constraints[i])
    return


# NOTE: this is to initialize the board
def get_least_conflicts_y(x, n, assignment, possible):
    # conflict_list is the list of min_conflict y-values
    # min_count is the current lowest cell conflict number
    if x == 1:
        return choice(possible)

    conflict_list, min_count = [possible[0]], get_num_conflicts([x, possible[0]], assignment)

    # for the rest of the board
    # for i in range(2, n+1):
    for i in possible[1:]:
        count = get_num_conflicts([x, i], assignment)
        # update the min_count and list
        if min_count > count:
            min_count = count
            conflict_list = [i]
        elif min_count == count:
            conflict_list.append(i)

    # return conflict_list[randint(0, len(conflict_list) - 1)]
    return choice(conflict_list)

# basically the same as the function above
def conflicts(var, v, n, csp, not_possible):
    x, y = var, v
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

    clist = list(set(conflict_list) - set(not_possible))
    if clist != []:
        return choice(clist)

    # return conflict_list[randint(0, len(conflict_list) - 1)]
    return choice(conflict_list)


# functions to create and print the board
def create_board(n):
    return [['-' for i in range(n)] for j in range(n)]

def print_board(board):
    for x in board:
        for y in x:
            print(y, end=' ')
        print()
    return
