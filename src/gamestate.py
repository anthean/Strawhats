import sys

import menus
from player import Player
from sprite import Sprite
from window_settings import *


class GameState:
    def __init__(self):
        self.name = ""
        self.player = None
        self.difficulty = 3
        self.score = 0
        self.game_over = False
        self.sprites = pygame.sprite.OrderedUpdates()

    def set_name(self, name):
        menus.SOUND.play_event()
        self.name = name.upper()

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def set_player(self, pcolor):
        idle = Sprite(pcolor + "idle.png", 5, upscale=2)
        run = Sprite(pcolor + "run.png", 6, upscale=2)
        jump = Sprite(pcolor + "jump.png", 2, upscale=2)
        crouch = Sprite(pcolor + "crouch.png", 3, upscale=2)
        death = Sprite(pcolor + "death.png", 8, upscale=2)
        ps = {"idle": idle, "run": run, "jump": jump, "crouch": crouch, "death": death}
        self.player = Player(ps, self.difficulty)

    def set_score(self, score):
        self.score = score
