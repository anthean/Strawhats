from player import Player


class GameState:
    def __init__(self):
        self.name = ''
        self.player = Player()
        self.score = 0
        self.game_over = False

    def new_game(self):
        self.set_name('')
        self.set_score(0)

    # Setters
    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score

    # Getters
    def name(self) -> str:
        return self.name

    def score(self) -> int:
        return self.score

    def game_over(self) -> bool:
        return self.game_over
