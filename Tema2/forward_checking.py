import model_util

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
    if (i, j) in model_util.par_pos:
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

import copy
def print_sol(state):
    if not model_util.is_valid(state):
        print("Inconsistent state")
        return
    state = copy.deepcopy(state)
    if solve(state[0]):
        print("Solution found:")
        for row in state[0]:
            print(row)
    else:
        print("No solution found.")

# print_sol(model_util.problem)