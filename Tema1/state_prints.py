import model
import copy
import math

def pretty_print(state):
    n = int(math.sqrt(len(state[0])))
    for i in range(0, n):
        print(state[0][(i*n):((i+1)*n)])
    print("=========")


def print_solution(state, solution):
    pretty_print(state)

    temp_state = copy.deepcopy(state)

    for i in solution:
        temp_state = model.transition(temp_state,i)
        pretty_print(temp_state)