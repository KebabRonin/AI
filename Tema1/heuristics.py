import math


# def hamming(state):
# 	s = list(filter(lambda x: x > 0, state[0]))
# 	score = 0
#
# 	last = s[0]
# 	for cu in s[1:]:
# 		if cu < last:
# 			score += 1
# 		else:
# 			last = cu
# 	return score


def manhattan(state):
    s = list(filter(lambda x: x > 0, state[0]))
    score = 0

    for index, cu in enumerate(s):
        score += abs(cu - (index + 1))
    return score


# print(hamming(([2,3,1,0,4,5,6,7,8], None)))
# print(manhattan(([2,3,1,0,4,5,6,7,8], None)))

def hamming(state):
    n = len(state)
    correct = [i for i in range(1, n)]
    state_without_zero = [cell for cell in state if cell != 0]
    return sum(1 for i, j in zip(state_without_zero, correct) if i != j)  # Calculăm distanța Hamming

# test_state = [2, 3, 1, 0, 4, 5, 6, 7, 8]
# distance = hamming(test_state)
# print("Distanța Hamming pentru starea de test:", distance)

def straight_line_distance(state):
    elements, last_move = state
    n = int(math.sqrt(len(elements)))
    score = 0

    for i, tile in enumerate(elements):
        if tile != 0:
            goal_row = tile // n
            goal_col = tile % n
            current_row = i // n
            current_col = i % n
            score += math.sqrt((goal_row - current_row) ** 2 + (goal_col - current_col) ** 2)

    return score


def chebyshev_distance(state):
    elements, last_move = state
    n = int(math.sqrt(len(elements)))
    score = 0

    for i, tile in enumerate(elements):
        if tile != 0:
            goal_row = tile // n
            goal_col = tile % n
            current_row = i // n
            current_col = i % n
            score = max(score, max(abs(goal_row - current_row), abs(goal_col - current_col)))

    return score
