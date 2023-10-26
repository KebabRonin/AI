import model
import heuristics
import model
import state_prints


def greedy(initial_state, heuristic):
    current_state = initial_state
    visited_states = []
    steps = 0
    while not model.is_final(current_state):
        possible_moves = [num for num in current_state[0] if model.validate(current_state, num)]
        best_move = None
        best_score = float('inf')
        for move in possible_moves:
            new_state = model.transition(current_state, move)
            h = heuristics.hamming(new_state[0])
            if h < best_score and new_state[0] not in visited_states:
                best_score = h
                best_move = move
        if best_move is None:
            raise Exception("No valid moves available after " + str(steps) + " steps")
        visited_states.append(current_state[0])
        state_prints.pretty_print(current_state)
        current_state = model.transition(current_state, best_move)
        steps += 1
    return {'current_state': current_state, 'steps': steps}


initial_state = ([2, 7, 5, 0, 8, 4, 3, 1, 6], None)
result = greedy(initial_state, heuristics.hamming)
print("Solution using Hamming Distance:", result['current_state'])
print("Steps:", result['steps'])