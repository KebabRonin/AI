import model_util

def forward_check(problem, var, value):
    return model_util.get_vars(problem[0], problem[1])

def solve(problem, variables):
    board, parity_pos = problem
    if len(variables) == 0:
        return True
    model_util.mrv(variables)

    (i, j), dom = variables[0]
    dom = copy.deepcopy(dom)
    
    for value in dom:
        board[i][j] = value
        variables = forward_check(problem)
        if variables is None:
            board[i][j] = 0
        elif solve(problem, variables):
            return True
        board[i][j] = 0
    return False

import copy
def print_sol(state):
    if not model_util.is_valid(state):
        print("Inconsistent state")
        return
    state = copy.deepcopy(state)
    variables = forward_check(state)
    if solve(state, variables):
        print("Solution found:")
        for row in state[0]:
            print(row)
    else:
        print("No solution found.")

print_sol(model_util.problem)