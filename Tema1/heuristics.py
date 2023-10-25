def hamming(state):
	s = list(filter(lambda x: x > 0, state[0]))
	score = 0

	last = s[0]
	for cu in s[1:]:
		if cu < last:
			score += 1
		else:
			last = cu
	return score


def manhattan(state):
	s = list(filter(lambda x: x > 0, state[0]))
	score = 0

	for index, cu in enumerate(s):
		score += abs(cu - (index + 1))
	return score

# print(hamming(([2,3,1,0,4,5,6,7,8], None)))
# print(manhattan(([2,3,1,0,4,5,6,7,8], None)))