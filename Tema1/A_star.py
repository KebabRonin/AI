import model
import math


def A_star(initial_state, heuristic):
	unexplored = [(initial_state, 0, heuristic(initial_state))]
	explored = []
	best_score = 100

	# here, a state is (base_state, distance_till_state, heuristic)

	while len(unexplored) > 0:
		# print(f"before:\n	expl:{explored}\n	unex:{unexplored}\n\n")
		current_state, d, h = unexplored.pop(0)

		if model.is_final(current_state):
			best_score = d + h

		explored.append((current_state, d, h))

		# add all neighbours
		for dir in model.dirs:
			if model.validate(current_state, dir):
				t = model.transition(current_state, dir)
				like_me_unex = list(filter(lambda st: st[0] == t, unexplored))
				like_me_ex = list(filter(lambda st: st[0] == t, explored))
				if 0 < len(like_me_ex):
					if len(like_me_ex) > 1:
						print("Duplicates in explored states")
					if like_me_ex[0][1] > d + 1:
						explored.append((t, d + 1, heuristic(t)))
						explored.remove(like_me_ex[0])
				elif 0 < len(like_me_unex):
					if len(like_me_unex) > 1:
						print("Duplicates in unexplored states")
					if like_me_unex[0][1] > d + 1:
						unexplored.append((t, d + 1, heuristic(t)))
						unexplored.remove(like_me_unex[0])
				else:
					unexplored.append((t, d + 1, heuristic(t)))


		unexplored = list(sorted(filter(lambda st: (st[1] + st[2]) < best_score,unexplored),
						   key = lambda st: (st[1] + st[2])))
		# print(f"after:\n	unex:{unexplored[0:3]}\n\n")

	# print("gata de cautat")

	final_states = list(filter(lambda s: model.is_final(s[0]) and s[1] + s[2] == best_score, explored))
	if len(final_states) == 0:
		return None
	final_state = final_states[0]
	d = final_state[1]
	moves = []
	while final_state[1] != 0:
		moves.append(final_state[0][1])
		t = model.reverse_transition(final_state[0])
		final_states = list(sorted(filter(lambda s: s[0][0] == t, explored), key=lambda t: t[1]))
		if len(final_states) == 0:
			print("ceva ciudat", final_states, t, explored)
			return
		final_state = final_states[0]
		d = final_state[1]

	return moves

# import heuristics
# print(A_star(model.init([2, 5, 3,
#         1, 0, 6,
#         4, 7, 8]), heuristic=heuristics.manhattan))
# print(A_star(model.init([2, 7, 5,
#         0, 8, 4,
#         3, 1, 6]), heuristic=heuristics.manhattan))