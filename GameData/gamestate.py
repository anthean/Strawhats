# TODO: COMPLETE GAMESTATE IMPLEMENTATION


class GameState:
    def __init__(self):
        self._name = ''
        self._score = 0
        self._game_over = False

    def new_game(self):
        self.set_name('')
        self.set_score(0)

    # Setters
    def set_name(self, name):
        self._name = name

    def set_score(self, score):
        self._score = score

    # Getters
    def name(self) -> str:
        return self._name

    def score(self) -> int:
        return self._score

    def game_over(self) -> bool:
        return self._game_over
