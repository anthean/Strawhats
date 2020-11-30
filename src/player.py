import pygame_functions as pgf


class Player:
    def __init__(self, pcolor, difficulty):
        self.idle_sprite = pgf.makeSprite(pcolor+'idle.png', 5)
        self.run_sprite = pgf.makeSprite(pcolor+'run.png', 6)
        self.jump_sprite = pgf.makeSprite(pcolor+'jump.png', 2)
        self.crouch_sprite = pgf.makeSprite(pcolor+'crouch.png', 3)
        self.death_sprite = pgf.makeSprite(pcolor+'death.png', 8)
        self.immune_system = difficulty
