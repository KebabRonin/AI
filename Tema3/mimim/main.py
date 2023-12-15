import copy
import game


def minimax(state: game.State, heuristic, levels, move= None, level= 0):
    if level == levels or state.is_final():
        return (move, heuristic(state))
    
    s = copy.deepcopy(state)
    if move:
        # print(s.remaining, move)
        s.make_transition(move)

    moves = [minimax(s, heuristic, levels, move= next_move, level= level + 1) for next_move in s.get_remaining_choices()]

    if len(moves) == 0:
        return (move, heuristic(s))
    
    if level % 2 == 0:
        return min(moves, key= lambda m: m[1])
    else:
        return max(moves, key= lambda m: m[1])


def ai_driver(heuristic, levels):
    def _ai_driver(state: game.State):
        move, score = minimax(state, heuristic, levels= levels)
        return move

    return _ai_driver


def human_driver(state: game.State):
    while True:
        resp = input("Choose a number:")
        try:
            return int(resp)
        except:
            print("Please choose a number")


def heuristic(state: game.State):
    if state.is_winner(0):
        return 100
    if state.is_winner(1):
        return -100
    
    score = 0
    my_ch = state.player_numbers[0]
    for i in range(len(my_ch)):
        for j in range(i+1, len(my_ch)):
            for k in range(j+1, len(my_ch)):
                score += my_ch[i] + my_ch[j] + my_ch[k]
    my_ch = state.player_numbers[1]
    for i in range(len(my_ch)):
        for j in range(i+1, len(my_ch)):
            for k in range(j+1, len(my_ch)):
                score -= my_ch[i] + my_ch[j] + my_ch[k]
    return score


game.play(ai_driver(heuristic= lambda x: len(x.get_remaining_choices()), levels= 3), human_driver)