import model
import state_prints as sp
import time

import IDDFS
import A_star


def test_algo(algo, *args):
    dirs = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    examples = [
        [2, 5, 3,
         1, 0, 6,
         4, 7, 8],

        [2, 7, 5,
         0, 8, 4,
         3, 1, 6],

        [8, 6, 7,
         2, 5, 4,
         0, 3, 1]]
    #               6 steps                       23 steps                      31 steps
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


#test_algo(IDDFS.IDDFS)
test_algo(A_star.A_star, A_star.hamming)