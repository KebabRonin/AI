import math


def hamming(state):
	s = list(filter(lambda x: x > 0, state[0]))
	n = int(math.sqrt(len(s)))
	score = 0

	last = s[0]
	for cu in s[1:]:
		if cu < last:
			score += 1
		else:
			last = cu
	return score


# hamming(([2,3,1,0,4,5,6,7,8], None))