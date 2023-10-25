import math
import copy

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

dirs = [UP, RIGHT, DOWN, LEFT]


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


def test_model():
    print("is_final [8, 6, 7, 2, 5, 4, 0, 3, 1]:", is_final(([8, 6, 7, 2, 5, 4, 0, 3, 1], None)))
    print("is_final [1, 2, 0, 3, 4, 5, 6, 7 ,8]:", is_final(([1, 2, 0, 3, 4, 5, 6, 7 ,8], None)))

    state = init([8, 6, 7, 2, 5, 4, 0, 3, 1])
    print(state)
    dirs = ['UP', 'RIGHT', 'DOWN', 'LEFT']

    for i in range(0,4):
        val = validate(state, i)
        print("can go ",dirs[i],"?:", val)
        if val:
            new_state = transition(state, i)
            print(state, " - > ", new_state)