import model_util

def forward_check(problem):
    return model_util.get_vars(problem[0], problem[1])

def solve(problem):
    board, parity_pos = problem
    variables = forward_check(problem)

    if variables is None:
        return False
    elif len(variables) == 0:
        return True

    model_util.mrv(variables)

    (i, j), dom = variables[0]
    dom = copy.deepcopy(dom)
    
    for value in dom:
        board[i][j] = value
        if solve(problem):
            return True
        board[i][j] = 0
    return False

import copy
def print_sol(state):
    if not model_util.is_valid(state):
        print("Inconsistent state")
        return
    state = copy.deepcopy(state)
    if solve(state):
        print("Solution found:")
        for row in state[0]:
            print(row)
    else:
        print("No solution found.")

# print_sol(model_util.problem)