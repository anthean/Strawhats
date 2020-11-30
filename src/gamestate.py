import pygame_functions as pgf
from math import sqrt, ceil
from collections import namedtuple
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
        pgf.setAutoUpdate(False)
        self.frame = 0
        self.next_frame = pgf.clock()
        self.score = 0
        self.game_over = False
        self.load_background()
        pgf.endWait()


    def load_background(self):
        bg = pgf.makeSprite('./assets/sprites/STAGE/stage.png')
        pgf.transformSprite(bg, (WIDTH, HEIGHT))
        pgf.moveSprite(bg, 0, 0)
        pgf.showSprite(bg)

    def set_player(self, pcolor, difficulty):
        PS = namedtuple('PS', ['idle', 'run', 'jump', 'crouch', 'death'])
        idle = pgf.makeSprite(pcolor+'idle.png', 5)
        run = pgf.makeSprite(pcolor+'run.png', 6)
        jump = pgf.makeSprite(pcolor+'jump.png', 2)
        crouch = pgf.makeSprite(pcolor+'crouch.png', 3)
        death = pgf.makeSprite(pcolor+'death.png', 8)
        ps = PS(idle, run, jump, crouch, death)
        self.player = Player(ps, difficulty)

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score
