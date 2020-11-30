import pygame_functions as pgf
from window_settings import *


class Player:
    def __init__(self, ps, difficulty):
        self.ps = ps
        self.current_sprite = self.ps.idle
        self.immune_system = difficulty
        self.x = PX(0.5)
        self.y = PY(0.2)
        self.speed = PX(0.1)
        self.frame_dict = {self.ps.idle:5, self.ps.run:6, self.ps.jump:2, self.ps.crouch:3, self.ps.death:8}
        self.frame = 0
        self.next_frame = pgf.clock()
        
