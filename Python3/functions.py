from random import choice

# CLASSES #
class Board():
    """
    ------------------------------------------------------
    A Board object that keeps track of the conflicting
    queens and can update their constraints.
    ------------------------------------------------------
    """
    def __init__(self, n):
        self._n = n
        self._queen_rows = {i: set() for i in range(1, self._n+1)}
        self._queen_updiag = {i: set() for i in range(1, 2 * self._n)}
        self._queen_downdiag = {i: set() for i in range(1, 2 * self._n)}

    def set_queen(self, x, y, constraints):
        # get the combined set of conflicted queens
        combined = self._queen_rows[y] | self._queen_updiag[y+(x-1)] | self._queen_downdiag[y + (self._n - x)]

        # update the number of conflicts for each queen by 1
        for i in combined:
            constraints[i] += 1

        # add the queen to the board
        self._queen_rows[y].add(x)
        self._queen_updiag[y+(x-1)].add(x)
        self._queen_downdiag[y+(self._n - x)].add(x)

        # update number of conflicts
        constraints[x] = len(combined)
        return

    def remove_queen(self, x, y, constraints):
        # get the combined set of conflicted queens
        combined = self._queen_rows[y] | self._queen_updiag[y+(x-1)] | self._queen_downdiag[y + (self._n - x)]

        # update the number of conflicts for each queen by 1
        for i in combined:
            constraints[i] -= 1

        # removes the queen from the board
        self._queen_rows[y].remove(x)
        self._queen_updiag[y+(x-1)].remove(x)
        self._queen_downdiag[y+(self._n - x)].remove(x)

        constraints[x] = 0
        return

    def get_num_conflicts(self, x, y):
        # get the combined set of conflicted queens
        combined = self._queen_rows[y] | self._queen_updiag[y+(x-1)] | self._queen_downdiag[y + (self._n - x)]

        return len(combined)


class CSP():
    """
    ------------------------------------------------------
    A CSP object that holds the variables, domains and
    constraints.
    ------------------------------------------------------
    """
    def __init__(self, variables , domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints


# FUNCTIONS #
def min_conflicts(csp, n, board, max_steps=100):
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
    past_queen = None
    x = 50 if n >= 100 else (n//2)
    for i in range(1, max_steps+1):
        # get the list of conflcited queens from the csp constraints
        # NOTE: constraints is the list of conflicted queens
        conflicted = [i for i, j in csp.constraints.items() if j != 0]
        # if there are not more conflicting queens then the problem is sovled
        if conflicted == []:
            print('Steps: {}'.format(i))
            return csp
        if past_queen is not None and past_queen in conflicted:
            conflicted.remove(past_queen)
        # get a random queen from the conflicted list
        var = choice(conflicted)
        past_queen = var
        board.remove_queen(var, csp.domains[var], csp.constraints)
        if var in past_var:
            if csp.domains[var] not in past_var[var]:
                past_var[var].append(csp.domains[var])
        else:
            past_var[var] = [csp.domains[var]]

        value = conflicts(var, csp.domains[var], n, csp, past_var[var], board)
        if len(past_var[var]) >= x: past_var[var].pop(0)

        csp.domains[var] = value
        board.set_queen(var, value, csp.constraints)
    return False


# NOTE: this is to initialize the board
def get_least_conflicts_y(x, n, assignment, possible, board):
    # conflict_list is the list of min_conflict y-values
    # min_count is the current lowest cell conflict number

    conflict_list, min_count = [possible[0]], board.get_num_conflicts(x, possible[0])

    # for the rest of the board
    for i in possible[1:]:
        count = board.get_num_conflicts(x, i)
        # update the min_count and list
        if min_count > count:
            min_count = count
            conflict_list = [i]
        elif min_count == count:
            conflict_list.append(i)

    return choice(conflict_list)


# basically the same as the function above
def conflicts(var, v, n, csp, not_possible, board):
    x, y = var, v
    conflict_list, min_count = [], None

    for i in range(1, n+1):
        if i == y: continue
        count = board.get_num_conflicts(x, i)
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
