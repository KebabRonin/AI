import random, matplotlib.pyplot as plt

LINS = 7
COLS = 10
FINAL_STATE = (3, 7)
REWARD = [[-1 for _ in range(COLS)] for _ in range(LINS)]
REWARD[FINAL_STATE[0]][FINAL_STATE[1]] = 10_000
DIRS = [(-1,0), (0,1), (1,0), (0,-1)]
NAMES=["down ", "right", "up   ", "left "]
WINDS = [0,0,0,1,1,1,2,2,1,0]



def clamp(x, high):
    return max(0, min(high, x))

def Q(state, act):
    x, y = transition(state, act)
    return qtable[x][y]

def transition(state, act):
    x, y = state
    dir = DIRS[act]
    return (clamp(x+dir[0]-WINDS[y], LINS-1), clamp(y+dir[1], COLS-1))


def learn(qtable, eps, episodes, start_pos, lr, gamma):
    qtable[FINAL_STATE[0]][FINAL_STATE[1]] = REWARD[FINAL_STATE[0]][FINAL_STATE[1]]
    history = []
    for ep in range(episodes):
        state = start_pos
        while state != FINAL_STATE:
            qchoices = [Q(state, dir) for dir in range(len(DIRS))]
            # qtable[state[0]][state[1]] = REWARD[state[0]][state[1]] + max(qchoices)
            qtable[state[0]][state[1]] = qtable[state[0]][state[1]] + lr*(REWARD[state[0]][state[1]] + gamma*max(qchoices) - qtable[state[0]][state[1]])

            if random.random() < eps:
                next_dir = random.randint(0, 3)
            else:
                next_dir = random.choice(list(filter(lambda x: x[1] == max(qchoices), enumerate(qchoices))))[0]
            state = transition(state, next_dir)
        if ep%25==0:
            history.append(sum([sum(l) for l in qtable]))
    plt.plot(history)
    plt.xticks(range(0, len(history), 4), [str((x+1)*25) for x in range(0, len(history), 4)])





qtable = [[0 for _ in range(COLS)] for _ in range(LINS)]
learn(qtable, eps=0.5, episodes=1000, start_pos=(3,0), lr=0.2, gamma=0.8)



# Afisari
def afisare(qtable):
    for l in qtable:
        print(l)


    dir_choice = [['' for _ in range(COLS)] for _ in range(LINS)]
    for i in range(LINS):
        for j in range(COLS):
            qchoices = [Q((i, j), dir) for dir in range(len(DIRS))]
            dir_choice[i][j] = NAMES[random.choice(list(filter(lambda x: x[1] == max(qchoices), enumerate(qchoices))))[0]]
    dir_choice[FINAL_STATE[0]][FINAL_STATE[1]] = 'goal '

    for l in dir_choice:
        print(l)


    plt.matshow(qtable)
    plt.show()

    #normalize:
    # minim = min([min(list(filter(lambda x: x > 0, l))) for l in qtable])

    # for i in range(LINS):
    #     for j in range(COLS):
    #         if qtable[i][j] > 0:
    #             qtable[i][j] += -minim + 20

afisare(qtable)