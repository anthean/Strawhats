from sprite import Sprite
from window_settings import *


class Mobs:
    def __init__(self):
        self.mob_list = []

    def update(self, sprites, mob=False):
        if mob:
            self.addmob(mob)

        self.updatemobs(sprites)

        return sprites

    def addmob(self, mob):
        self.mob_list.append(mob)

    def updatemobs(self, sprites):
        for i, mob in enumerate(self.mob_list):
            if mob.isdead():
                self.mob_list.pop(i)
                sprites.remove(mob)
            else:
                None
