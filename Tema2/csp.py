import copy
"""
Variabile: pozitiile din tabla initiala care sunt 0
Domenii: {1..9}
Restrictii: Nu se poate repeta aceeasi cifra pe linie, coloana, sau intr-unul din patratele de 3x3
            De asemenea, pe pozitiile marcate pot fi doar cifre pare
"""
initial_board = [
    [8, 4, 0, 0, 5, 0, 0, 0, 0],
    [3, 0, 0, 6, 0, 8, 0, 4, 0],
    [0, 0, 0, 4, 0, 9, 0, 0, 0],
    [0, 2, 3, 0, 0, 0, 9, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 9, 8, 0, 0, 0, 1, 6, 0],
    [0, 0, 0, 5, 0, 3, 0, 0, 0],
    [0, 3, 0, 1, 0, 6, 0, 0, 7],
    [0, 0, 0, 0, 2, 0, 0, 1, 3]
]
par_pos = [(0, 6), (2, 2), (2, 8), (3, 4), (4, 3), (4, 5), (5, 4), (6, 0), (6, 6), (8, 2)]

def val_set(board, parity_pos, i, j):
    if (i,j) in parity_pos:
        set = {val for val in range(2, 10, 2)}
    else:
        set = {val for val in range(1, 10)}

    sub_i, sub_j = i//3*3, j//3*3
    set -= {board[i][t] for t in range(9) if t != i} | \
           {board[t][j] for t in range(9) if t != j} | \
           {board[a][b] for a in range(sub_i, sub_i+3) for b in range(sub_j, sub_j+3) if a != i and b != j}
    return set

def get_vars(board, parity_pos):
    l = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                vals = val_set(board, parity_pos, i, j)
                if len(vals) == 0:
                    return None
                l.append([(i,j),vals])
    return l

def get_neighbours(var1, variables):
    l = []
    for var2, _ in variables:
                if var1 != var2 and ((var1[0]//3 == var2[0]//3 and var1[1]//3 == var2[1]//3) or var1[0] == var2[0] or var1[1] == var2[1]):
                    l.append(var2)
    return l

def arc_consistency(variables):
    queue = []
    for var1, dom in variables:
            queue += [(var1, v) for v in get_neighbours(var1, variables)]
    # print("Q: \n",queue)
    while len(queue) > 0:
        (var1, var2) = queue.pop(0)
        dom = list(filter(lambda x: x[0] == var1, variables))[0][1]
        dom2 = list(filter(lambda x: x[0] == var2, variables))[0][1]

        if len(dom2) == 1 and len(dom2 & dom) > 0:
            dom -= dom2
            l = [(var1, v) for v in get_neighbours(var1, variables)]
            queue += [var for var in l if var not in queue]

mrv = lambda vars: vars.sort(key = lambda var: len(var[1]))
variables = get_vars(initial_board, par_pos)
mrv(variables)

problem = (initial_board, par_pos, variables)
cvar = copy.deepcopy(variables)
p_v = lambda l: {k:v for k, v in l}

print(p_v(variables))
print("=========================")
arc_consistency(cvar)
mrv(cvar)
print(p_v(cvar))

def forward_check(variables, i, j, value):
    for k in range(9):
        if k != j and variables[i][k] == value:
            return False
        if k != i and variables[k][j] == value:
            return False
    sub_i, sub_j = i//3*3, j//3*3
    for a in range(sub_i, sub_i+3):
        for b in range(sub_j, sub_j+3):
            if a != i and b != j and variables[a][b] == value:
                return False
    if (i, j) in par_pos:
        if value % 2 != 0:
            return False
    return True

def get_unassigned_variable(variables):
    min_legal_values = float('inf')
    selected_i, selected_j = None, None
    for i in range(9):
        for j in range(9):
            if variables[i][j] == 0:
                legal_values = [value for value in range(1, 10) if forward_check(variables, i, j, value)]
                if len(legal_values) < min_legal_values:
                    min_legal_values = len(legal_values)
                    selected_i, selected_j = i, j
    return selected_i, selected_j

def solve(variables):
    i, j = get_unassigned_variable(variables)
    if i is None and j is None:
        return True
    for value in range(1, 10):
        if forward_check(variables, i, j, value):
            variables[i][j] = value
            if solve(variables):
                return True
            variables[i][j] = 0
    return False

ib = copy.deepcopy(initial_board)
if solve(ib):
    print("Solution found:")
    for row in ib:
        print(row)
else:
    print("No solution found.")

def solve_arc(board, parity_pos):
    variables = get_vars(board, parity_pos)
    arc_consistency(variables)

    if len(variables) == 0:
        return True

    mrv(variables)

    i, j = variables[0][0]
    dom = copy.deepcopy(variables[0][1])

    for value in dom:
        if i == 8 and j == 3:
            print(dom)
        board[i][j] = value
        if solve_arc(board, parity_pos):
            return True
        board[i][j] = 0
    return False


ib = copy.deepcopy(initial_board)
if solve_arc(ib, par_pos):
    print("Solution found:")
    for row in ib:
        print(row)
else:
    print("No solution found.")