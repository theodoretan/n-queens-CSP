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

# print()
csp = CSP(variables, domains, constraints)

assignment = min_conflicts(csp, n, max_steps=1000)
end_time = time.time()

print(end_time - start_time)
print()

if not assignment:
    print(assignment)
else:
    # b = create_board(n)
    # for key, value in assignment.domains.items():
    #     b[value[1] - 1][value[0] - 1] = 'Q'
    # print_board(b)
    pass
