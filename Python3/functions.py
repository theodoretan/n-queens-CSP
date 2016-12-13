from random import choice

# CLASSES #
class Board:
    """
    ------------------------------------------------------
    A Board object that keeps track of the conflicting
    queens and can update their constraints.
    ------------------------------------------------------
    """
    def __init__(self, n):
        self._n = n
        self._queen_rows = {i: set() for i in range(1, self._n+1)}
        self._queen_posdiag = {i: set() for i in range(1, 2 * self._n)}
        self._queen_negdiag = {i: set() for i in range(1, 2 * self._n)}

    def set_queen(self, x, y, constraints):
        """
        ------------------------------------------------------
        Set a queen on the board.
        ------------------------------------------------------
        Inputs:
            x - the x value on the board
            y - the y value on the board
            constraints - the dict of conflicts for each
                queen
        ------------------------------------------------------
        """
        # get the combined set of conflicted queens
        combined = self._queen_rows[y] | self._queen_posdiag[y+(x-1)] | self._queen_negdiag[y + (self._n - x)]

        # update the number of conflicts for each queen by 1
        for i in combined:
            constraints[i] += 1

        # add the queen to the board
        self._queen_rows[y].add(x)
        self._queen_posdiag[y+(x-1)].add(x)
        self._queen_negdiag[y+(self._n - x)].add(x)

        # update number of conflicts
        constraints[x] = len(combined)
        return

    def remove_queen(self, x, y, constraints):
        """
        ------------------------------------------------------
        Removes a queen on the board.
        ------------------------------------------------------
        Inputs:
            x - the x value on the board
            y - the y value on the board
            constraints - the dict of conflicts for each
                queen
        ------------------------------------------------------
        """
        # get the combined set of conflicted queens
        combined = self._queen_rows[y] | self._queen_posdiag[y+(x-1)] | self._queen_negdiag[y + (self._n - x)]

        # update the number of conflicts for each queen by 1
        for i in combined:
            constraints[i] -= 1

        # removes the queen from the board
        self._queen_rows[y].remove(x)
        self._queen_posdiag[y+(x-1)].remove(x)
        self._queen_negdiag[y+(self._n - x)].remove(x)

        # update the number of conflicts
        constraints[x] = 0
        return

    def get_num_conflicts(self, x, y):
        """
        ------------------------------------------------------
        Get the number of conflicts for a point on the
        board.
        ------------------------------------------------------
        Inputs:
            x - the x value on the board
            y - the y value on the board
        Returns:
            c - the number of conflicted queens
        ------------------------------------------------------
        """
        # get the combined set of conflicted queens
        combined = self._queen_rows[y] | self._queen_posdiag[y+(x-1)] | self._queen_negdiag[y + (self._n - x)]

        return len(combined)


class CSP:
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


class Colours:
    """
    ------------------------------------------------------
    Colours for the terminal printing.
    ------------------------------------------------------
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# FUNCTIONS #
def min_conflicts(csp, n, board, max_steps=100):
    """
    ------------------------------------------------------
    Min-Conflicts algorithm for solving CSPs by
    local search.
    ------------------------------------------------------
    Inputs:
        csp - a CSP with components(X, D, C)
        n - the number of queens
        board - the board object keeping track of the
            queens in conflict
        max_steps - the number of steps allowed before
            giving up
    Returns:
        A solution or failure (False)
    ------------------------------------------------------
    """
    # Tabu Search list and variable to avoid repeating moves
    past_var = {}
    past_queen = None

    # sets the size of the tabu list
    x = 50 if n >= 100 else (n//2)

    for i in range(1, max_steps+1):
        # get the list of conflcited queens from the csp constraints
        conflicted = [i for i, j in csp.constraints.items() if j != 0]

        # if there are not more conflicting queens then the problem is sovled
        if conflicted == []:
            print('Steps: {}'.format(i))
            return csp

        # remove the past queen from the search space
        if past_queen is not None and past_queen in conflicted:
            conflicted.remove(past_queen)

        # get a random queen from the conflicted list and remove it from the board
        var = choice(conflicted)
        past_queen = var
        board.remove_queen(var, csp.domains[var], csp.constraints)

        # set the queens position into the tabu list so we dont place it back here
        if var in past_var:
            if csp.domains[var] not in past_var[var]:
                past_var[var].append(csp.domains[var])
        else:
            past_var[var] = [csp.domains[var]]

        # get the position with the least conflicts
        value = conflicts(var, csp.domains[var], n, csp, past_var[var], board)
        if len(past_var[var]) >= x: past_var[var].pop(0)

        # set the queen back on the board
        csp.domains[var] = value
        board.set_queen(var, value, csp.constraints)
    return False


def get_least_conflicts_y(x, n, possible, board):
    """
    ------------------------------------------------------
    Get's the position with the least conflicts for the
    column.
    ------------------------------------------------------
    Inputs:
        x - the x value on the board
        n - the number of queens
        possible - the list of possible moves
        board - the board object keeping track of the
            queens in conflict
    Returns:
        y - the y value on the board
    ------------------------------------------------------
    """
    # the list of y values that have the least conflicts
    conflict_list, min_count = [possible[0]], board.get_num_conflicts(x, possible[0])

    # for the rest of the column find the positions with the least conflicts
    for i in possible[1:]:
        count = board.get_num_conflicts(x, i)
        # update the min_count and list
        if min_count > count:
            min_count = count
            conflict_list = [i]
        elif min_count == count:
            conflict_list.append(i)

    return choice(conflict_list)


def conflicts(var, v, n, csp, not_possible, board):
    """
    ------------------------------------------------------
    Get's the position with the least conflicts for the
    column.
    ------------------------------------------------------
    Inputs:
        var - the x value on the board (or queen)
        v - the current y value
        n - the number of queens
        csp - a CSP with components(X, D, C)
        not_possible - the tabu list for that column
        board - the board object keeping track of the
            queens in conflict
    Returns:
        y - the y value on the board
    ------------------------------------------------------
    """
    x, y = var, v
    conflict_list, min_count = [], None

    # check the column for the position with the least conflicts
    for i in range(1, n+1):
        # skip the position we just came from
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

    # if the conflict is has positions that the queen has not been to yet
    if clist != []:
        return choice(clist)

    # if there were no positions available for the queen choose a random one
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
