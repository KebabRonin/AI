import model


def A_star(initial_state, heuristic):
	unexplored = [(initial_state, 0, heuristic(initial_state))]
	explored = []
	best_score = 1000000

	# here, a state is (base_state, distance_till_state, heuristic)

	while len(unexplored) > 0:
		current_state, d, h = unexplored.pop(0)

		if model.is_final(current_state):
			best_score = d + h

		# add all neighbours
		for dir in model.dirs:
			if model.validate(current_state, dir):
				t = model.transition(current_state, dir)

				like_me = filter(lambda st: st[0] == t[0] and st[1] + st[2] < t[1] + t[2], unexplored)
				if 0 < len(like_me):
					unexplored.append((like_me[0][0], d + 1, heuristic(t)))
					unexplored.remove(like_me[0])

				unexplored.append((t, d + 1, heuristic(t)))

		explored.append((current_state, d, h))

		unexplored = list(sorted(filter(lambda st: (st[1] + st[2]) < best_score,unexplored),
						   key = lambda st: (st[1] + heuristic(st[0]))))
