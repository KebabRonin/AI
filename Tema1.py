"""

state = ([8, 6, 7, 2, 5, 4, 0, 3, 1], None)

Modelul ales contine un vector de n elemente care retine pozitiile pieselor
si inca un numar, care reprezinta ultima directie in care am mutat '0'.

La fiecare pas, pot alege dintre maxim 3 directii de mutat, NESW,
din care scot ultima piesa mutata.

Cum pentru a avea pozitia goala, trebuie sa fi mutat '0' in directia opusa
pasului precedent (UP - DOWN/ LEFT - RIGHT), inseamna ca toate directiile
care nu ies din matrice sunt valide, exceptand opusul directiei ultimei miscari.

Ex:
 0  1  2  3  4  5  6  7  8
[8, 6, 7, 2, 5, 4, 0, 3, 1]  |  last_move = None / UP / RIGHT / DOWN / LEFT

 8  6  7
 2  5  4
 0  3  1

Mutari valide: [UP, RIGHT]

Aleg UP

 0  1  2  3  4  5  6  7  8
[8, 6, 7, 0, 5, 4, 2, 3, 1]  |  last_move = UP

 8  6  7
 0  5  4
 2  3  1

Mutari valide: [UP, RIGHT] = [UP, RIGHT, DOWN] - (DOWN)
"""
import math
import copy
import time

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


def is_final(state):
    next_nr = 1
    for i in state[0]:
        if i == next_nr:
            next_nr += 1
        elif i != 0:
            return False
    return True


def init(matrix):
    n = int(math.sqrt(len(matrix)))

    if n ** 2 != len(matrix):
        print("Matrix is not square")
        return None

    seen_nrs = []

    for i in matrix:
        if not (0 <= i < n ** 2):
            print("Matrix contains numbers greater than n")
            return None
        if i in seen_nrs:
            print("Matrix contains duplicates")
            return None
        seen_nrs.append(i)

    return (matrix, None)


def validate(state, dir_to_move):
    if state[1] is not None and (dir_to_move != state[1] and dir_to_move % 2 == state[1] % 2):  # nu misc aceeasi piesa
        return False

    n = int(math.sqrt(len(state[0])))

    poz_0 = state[0].index(0)
    lin = poz_0 // n
    col = poz_0 %  n

    if lin > 0 and dir_to_move == UP:
        return True
    if col < (n - 1) and dir_to_move == RIGHT:
        return True
    if lin < (n - 1) and dir_to_move == DOWN:
        return True
    if col > 0 and dir_to_move == LEFT:
        return True

    return False


def transition(state, dir_to_move):

    n = int(math.sqrt(len(state[0])))

    poz_0 = state[0].index(0)
    poz_to_move = state[0].index(dir_to_move)

    new_matrix = copy.deepcopy(state[0])

    if dir_to_move == UP:
            poz_to_move = poz_0 - n
    if dir_to_move == RIGHT:
            poz_to_move = poz_0 + 1
    if dir_to_move == DOWN:
            poz_to_move = poz_0 + n
    if dir_to_move == LEFT:
            poz_to_move = poz_0 - 1

    new_matrix[poz_0] = new_matrix[poz_to_move]

    new_matrix[poz_to_move] = 0

    return (new_matrix, dir_to_move)


def __IDDFS__(state, current_depth, depth):
    #print(state, current_depth, depth)
    if current_depth == depth:
        if is_final(state):
            print("Am reusit", state)
            return []
        else:
            return None
    else:
        for move in [UP, RIGHT, DOWN, LEFT]:
            if validate(state, move):
                st = transition(state, move)
                rez = __IDDFS__(st, current_depth + 1, depth)
                if rez is not None:
                    return [move] + rez


def IDDFS(state):
    i = 0
    rez = __IDDFS__(state, 0, i)
    while rez is None:
        i += 1
        rez = __IDDFS__(state, 0, i)
    return rez


def pretty_print(state):
    n = int(math.sqrt(len(state[0])))
    for i in range(0, n):
        print(state[0][(i*n):((i+1)*n)])
    print("=========")


dirs = ['UP', 'RIGHT', 'DOWN', 'LEFT']


def print_solution(state, solution):
    pretty_print(state)

    temp_state = copy.deepcopy(state)

    for i in solution:
        temp_state = transition(temp_state,i)
        pretty_print(temp_state)


def test_model():
    print("is_final [8, 6, 7, 2, 5, 4, 0, 3, 1]:", is_final(([8, 6, 7, 2, 5, 4, 0, 3, 1], None)))
    print("is_final [1, 2, 0, 3, 4, 5, 6, 7 ,8]:", is_final(([1, 2, 0, 3, 4, 5, 6, 7 ,8], None)))

    state = init([8, 6, 7, 2, 5, 4, 0, 3, 1])
    print(state)

    for i in range(0,4):
        val = validate(state, i)
        print("can go ",dirs[i],"?:", val)
        if val:
            new_state = transition(state, i)
            print(state, " - > ", new_state)


def test_algo(algo):
    examples = [[2, 5, 3, 1, 0, 6, 4, 7, 8], [2, 7, 5, 0, 8, 4, 3, 1, 6], [8, 6, 7, 2, 5, 4, 0, 3, 1]]
    #               6 steps                       23 steps                      31 steps
    for example in examples:
        state = init(example)
        t = time.time()
        rez = algo(state)
        t = time.time() - t
        print(state, f"--{len(rez)} steps ({t}s) -->",list(map(lambda i: dirs[i-1], rez)))
        print_solution(state, rez)
        print()


test_algo(IDDFS)