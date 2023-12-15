import random

class NumberScrabble:
    def __init__(self):
        self.player_AI_numbers = []
        self.player_HUMAN_numbers = []
        self.turn = 'AI' if random.random() > 0.5 else 'HUMAN'

    def get_available_numbers(self):
        return [i for i in range(1, 10) if i not in self.player_AI_numbers + self.player_HUMAN_numbers]

    def is_game_over(self):
        return len(self.player_AI_numbers + self.player_HUMAN_numbers) >= 9 or self.is_winner('AI') or self.is_winner('HUMAN')

    def is_winner(self, player):
        if player == 'AI':
            chosen_numbers = self.player_AI_numbers
        else:
            chosen_numbers = self.player_HUMAN_numbers

        if len(chosen_numbers) < 3:
            return False

        for i in range(len(chosen_numbers)):
            for j in range(i + 1, len(chosen_numbers)):
                for k in range(j + 1, len(chosen_numbers)):
                    if chosen_numbers[i] + chosen_numbers[j] + chosen_numbers[k] == 15:
                        return True
        return False

    def play(self, player, number):
        # Validare
        if player != self.turn or number not in self.get_available_numbers():
            return False

        if player == 'AI':
            self.player_AI_numbers.append(number)
        else:
            self.player_HUMAN_numbers.append(number)

        self.turn = 'HUMAN' if game.turn == 'AI' else 'AI'

        return True
    
    def undo_play(self):
        self.turn = 'HUMAN' if game.turn == 'AI' else 'AI'
        if self.turn == 'AI':
            self.player_AI_numbers.pop()
        else:
            self.player_HUMAN_numbers.pop()


    def print_board(self):
        print("Jucătorul AI:", self.player_AI_numbers)
        print("Jucătorul HUMAN:", self.player_HUMAN_numbers)


def heuristic(self):
    a_combinations = 0
    b_combinations = 0

    if self.is_winner('AI'):
        a_combinations = 10000

    if self.is_winner('HUMAN'):
        b_combinations = 10000

    if b_combinations != a_combinations:
        return b_combinations - a_combinations
    else:
        scor = 0
        choices = (-1, 2, 3, 2, 3, 4, 3, 2, 3, 2)
        for i in self.player_HUMAN_numbers:
            scor -= choices[i]
        for i in self.player_AI_numbers:
            scor += choices[i]
        return scor


def minimax(state, depth, maximizing_player):
    if depth == 0 or state.is_game_over():
        # state.print_board()
        # print(heuristic(state))
        return heuristic(state)

    if maximizing_player:
        max_eval = float('-inf')
        for number in state.get_available_numbers():
            if state.play('HUMAN', number):
                eval = minimax(state, depth - 1, False)
                state.undo_play()
                max_eval = max(max_eval, eval)
        # state.print_board()
        return max_eval
    else:
        min_eval = float('inf')
        for number in state.get_available_numbers():
            if state.play('AI', number):
                eval = minimax(state, depth - 1, True)
                state.undo_play()
                min_eval = min(min_eval, eval)
        # state.print_board()
        return min_eval


def best_move(state):
    best_score = float('-inf')
    best_move = None
    for number in state.get_available_numbers():
        if state.play('AI', number):
            score = minimax(state, 5, False)
            state.undo_play()
            if score > best_score:
                best_score = score
                best_move = number
            elif score == best_score:
                best_move = random.choice([best_move, number])
    return best_move


def human_move(state):
    x = input("Introdu un numar:")
    while True:
        try:
            return int(x)
        except:
            x = input("Introdu un numar:")
            pass


game = NumberScrabble()
someone_won = False

while not game.is_game_over():
    if game.turn == 'AI':
        move = best_move(game)
    else:
        move = human_move(game)

    if game.play(game.turn, move):
        game.print_board()
        if game.is_winner('AI'):
            print("Jucătorul AI a câștigat!")
            someone_won = True
            break
        elif game.is_winner('HUMAN'):
            print("Jucătorul HUMAN a câștigat!")
            someone_won = True
            break
    else:
        print("Mutare invalidă! AIlege alt număr.")

if not someone_won:
    print("Remiză!")
