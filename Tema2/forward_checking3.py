import copy
import model_util

def forward_check(problem, variables, var):
    for x in var[1]:
        for v in model_util.get_neighbours(v[0]):


def solve(problem, variables):
    board, parity_pos = problem
    if len(variables) == 0:
        return True
    model_util.mrv(variables)

    (i, j), _ = variables[0]
    
    choice = forward_check(problem, variables, variables[0])
    if choice is None:
        return False
    else:
        board[i][j] = choice
    return solve(problem, variables)

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