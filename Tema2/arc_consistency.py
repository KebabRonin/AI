import copy
import model_util

def arc_consistency(variables):
    if variables is None:
        return
    
    queue = []
    for var1, dom in variables:
            queue += [(var1, v) for v in model_util.get_neighbours(var1, variables)]
    # print("Q: \n",queue)
    while len(queue) > 0:
        (var1, var2) = queue.pop(0)
        dom = list(filter(lambda x: x[0] == var1, variables))[0][1]
        dom2 = list(filter(lambda x: x[0] == var2, variables))[0][1]

        if len(dom2) == 1 and len(dom2 & dom) > 0:
            dom -= dom2
            l = [(var1, v) for v in model_util.get_neighbours(var1, variables)]
            queue += [var for var in l if var not in queue]

def solve_arc(state):
    board, parity_pos = state
    variables = model_util.get_vars(board, parity_pos)
    arc_consistency(variables)

    if variables is None:
        return False
    elif len(variables) == 0:
        return True

    model_util.mrv(variables)

    (i, j), dom = variables[0]
    dom = copy.deepcopy(dom)

    for value in dom:
        board[i][j] = value
        if solve_arc((board, parity_pos)):
            return True
        board[i][j] = 0
    return False

import copy
def print_sol(state):
    if not model_util.is_valid(state):
        print("Inconsistent state")
        return
    state = copy.deepcopy(state)
    if solve_arc(state):
        print("Solution found:")
        for row in state[0]:
            print(row)
    else:
        print("No solution found.")

# print_sol(model_util.problem)