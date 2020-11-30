import pygame_functions as pgf
from math import sqrt
from player import Player


class GameState:
    def __init__(self):
        self.screen_w = None
        self.screen_h = None
        self.name = ''
        self.player = None
        self.score = 0
        self.game_over = False

    def start(self, WIDTH, HEIGHT, FULLSCREEN):
        if FULLSCREEN: pgf.screenSize(WIDTH, HEIGHT, fullscreen=True)
        else: pgf.screenSize(WIDTH, HEIGHT)
        self.screen_w = WIDTH
        self.screen_h = HEIGHT
        self.score = 0
        self.game_over = False
        self.load_background()
        pgf.endWait()

    def load_background(self):
        bg = pgf.makeSprite('./assets/sprites/STAGE/stage.png')
        scale = int(sqrt(self.screen_w*self.screen_h/36864))
        pgf.transformSprite(bg, scale=scale)
        pgf.moveSprite(bg, 0, 0)
        pgf.showSprite(bg)

    def set_player(self, pcolor):
        self.player = Player(pcolor)

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score

