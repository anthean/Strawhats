import pygame_functions as pgf
from math import sqrt
from player import Player
from window_settings import *


class GameState:
    def __init__(self):
        self.name = ''
        self.player = None
        self.score = 0
        self.game_over = False

    def start(self):
        if FULLSCREEN: pgf.screenSize(WIDTH, HEIGHT, fullscreen=True)
        else: pgf.screenSize(WIDTH, HEIGHT)
        self.score = 0
        self.game_over = False
        self.load_background()
        pgf.endWait()

    def load_background(self):
        bg = pgf.makeSprite('./assets/sprites/STAGE/stage.png')
        scale = int(sqrt(WIDTH*HEIGHT/36864))
        pgf.transformSprite(bg, scale=scale)
        pgf.moveSprite(bg, 0, 0)
        pgf.showSprite(bg)

    def set_player(self, pcolor, difficulty):
        self.player = Player(pcolor, difficulty)

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score
