import copy

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

problem = copy.deepcopy((initial_board, par_pos))

def val_set(board, parity_pos, i, j):
    if (i,j) in parity_pos:
        set = {val for val in range(2, 10, 2)}
    else:
        set = {val for val in range(1, 10)}

    sub_i, sub_j = i//3*3, j//3*3
    set -= {board[i][t] for t in range(9) if t != j} | \
           {board[t][j] for t in range(9) if t != i} | \
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

def is_valid(state):
    for i in range(9):
        for j in range(9):
             if state[0][i][j] != 0 and state[0][i][j] not in val_set(state[0], state[1], i, j):
                  return False
    return True


mrv = lambda vars: vars.sort(key = lambda var: len(var[1]))