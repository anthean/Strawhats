class GameState:
    def __init__(self):
        self.name = ''
        self.score = 0

    def new_game(self):
        self.set_name('')
        self.set_score(0)

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score
