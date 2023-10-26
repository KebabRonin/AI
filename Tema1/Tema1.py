import model
import state_prints as sp
import time

import heuristics
import IDDFS
import greedy
import A_star


def test_algo(algo, *args):

    if args:
        print(f"{algo.__name__} with {args[0].__name__}".center(50,'='))
    else:
        print(f"{algo.__name__}".center(50,'='))

    dirs = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    examples = [
        [2, 5, 3,
        1, 0, 6,
        4, 7, 8],
        # ^^ 6 steps
        [2, 7, 5,
        0, 8, 4,
        3, 1, 6],
        # ^^ 23 steps
        # [8, 6, 7,
        # 2, 5, 4,
        # 0, 3, 1]
        # ^^ 31 steps
    ]

    for example in examples:
        state = model.init(example)
        t = time.time()
        rez = algo(state, *args)
        t = time.time() - t
        if rez is None:
            print(state, f"--No solution ({t}s) -->", rez)
        else:
            print(state, f"--{len(rez)} steps ({t}s) -->",list(map(lambda i: dirs[i-1], rez)))
        #sp.print_solution(state, rez)
        print()


test_algo(IDDFS.IDDFS)
test_algo(greedy.greedy, heuristics.manhattan)
test_algo(greedy.greedy, heuristics.hamming)
test_algo(greedy.greedy, heuristics.chebyshev_distance)
# test_algo(A_star.A_star, heuristics.hamming) # Nu merge