class State:
    def __init__(self):
        self.player_numbers = [[], []]
        self.player = 0

    def __str__(self):
        return f"Next: {'AB'[self.player]}\nScore A: {self.player_numbers[0]}\nScore B: {self.player_numbers[1]}\nRemaining: {self.get_remaining_choices()}\n"

    def is_winner(self, player):
        my_n = self.player_numbers[player]
        l = len(my_n)
        for i in range(0, l):
            for j in range(i+1, l):
                for k in range(j+1, l):
                    if my_n[i] + my_n[j] + my_n[k] == 15:
                        return True
        return False

    def is_final(self):
        return len(self.player_numbers[0]) + len(self.player_numbers[0]) == 9 or \
            self.is_winner(0) or self.is_winner(1)
    
    def result(self):
        if not self.is_final():
            return 'Ongoing'
        if len(self.player_numbers) == 0:
            return 'Draw'
        if self.is_winner(0):
            return 'Player A Wins'
        if self.is_winner(1):
            return 'Player B Wins'
        return 'Oopsie'
    
    def is_valid_transition(self, move):
        if self.is_final():
            return False
        p, c = move
        return p == self.player and c in self.get_remaining_choices()
    
    def make_transition(self, choice):
        self.player_numbers[self.player].append(choice)
        self.player = ~self.player

    def reverse_transition(self):
        self.player = ~self.player
        self.player_numbers[self.player].pop()

    def get_remaining_choices(self):
        return {i for i in range(1, 10)} - set(self.player_numbers[0]) - set(self.player_numbers[1])
        


def play(player1, player2, player1_name='A', player2_name='B'):
    state = State()
    players = [player1, player2]
    p = 0

    while not state.is_final():
        print(state)
        print("AB"[p], "has to move")
        c = players[p](state)

        while not state.is_valid_transition((p, c)):
            print("Invalid move, try again")
            c = players[p](state)
        else:
            state.make_transition(c)
            p = ~p
    else:
        print(state)
        print(state.result())