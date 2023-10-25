import model
import heuristics

def __greedy__(state, heuristic, current_depth, max_depth):

	if max_depth == current_depth:
		if model.is_final(state):
			return []
		else:
			return None

	choices = [model.transition(state, dir) for dir in model.dirs if model.validate(state, dir)]

	choices.sort(key = heuristic)
	# print(state, "->", list(map(lambda x: (x,heuristic(x)), choices)))

	for move in choices:
		rez = __greedy__(move, heuristic, current_depth + 1, max_depth)
		if rez is not None:
			return [move[1]] + rez


def greedy(state, heuristic):
    i = 0
    rez = __greedy__(state, heuristic, 0, i)
    while rez is None:
        i += 1
        rez = __greedy__(state, heuristic, 0, i)
    return rez

# print(greedy(([2,3,1,
# 			 0,4,5,
# 			 6,7,8], None), heuristics.hamming))