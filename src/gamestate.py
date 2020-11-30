from math import sqrt
import pygame_functions as pgf
from player import Player

class GameState:
    def __init__(self):
        self.name = ''
        self.player = None
        self.score = 0
        self.game_over = False

    def start(self, WIDTH, HEIGHT, FULLSCREEN):
        if FULLSCREEN: pgf.screenSize(WIDTH, HEIGHT, fullscreen=True)
        else: pgf.screenSize(WIDTH, HEIGHT)
        self.score = 0
        self.game_over = False
        bg = pgf.makeSprite('./assets/sprites/STAGE/stage.png')
        scale = int(sqrt(WIDTH*HEIGHT / 36864))
        pgf.transformSprite(bg, scale=scale)
        pgf.moveSprite(bg, 0, 0)
        pgf.showSprite(bg)
        pgf.endWait()

    def set_player(self, pcolor):
        self.player = Player(pcolor)

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score

    def name(self) -> str:
        return self.name

    def score(self) -> int:
        return self.score

    def game_over(self) -> bool:
        return self.game_over
