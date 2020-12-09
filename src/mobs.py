from sprite import Sprite
from window_settings import *
import random

class Mobs:
    def __init__(self):
        self.mob_list = []
        self.mobcount = 0

    def update(self, sprites, state, player, pplat):
        self.updatemobs(sprites, state, player, pplat)
        return sprites

    def addmob(self, mob):
        self.mobcount += 1
        self.mob_list.append(mob)

    def updatemobs(self, sprites, state, player, pplat):
        for i, mob in enumerate(self.mob_list):
            if mob.isdead():
                print('removing')
                sprites.remove(mob)
                self.mob_list.pop(i)
            else:
                mob.update(sprites, state, player, pplat)

    def getcount(self):
        return len(self.mob_list)