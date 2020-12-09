import random
import sys

import menus
from infected import Infected
from mobs import Mobs
from platforms import Platform
from player import Player
from projectile import Projectile
from sprite import Sprite
from window_settings import *

SPAWNDICT = {'lfloor': ((-PX(0.75)), (PY(0.82))), 'rfloor': ((PX(1.25)), (PY(0.82))), 'left': ((-PX(0.75)), (PY(0.222))), 'right': ((PX(1.25)), (PY(0.222)))}



class GameState:
    def __init__(self):
        self.name = ""
        self.player = None
        self.difficulty = 3
        self.score = 0
        self.game_over = False
        self.psprites = pygame.sprite.OrderedUpdates()
        self.projectile_sprites = pygame.sprite.OrderedUpdates()
        self.mob_sprites = pygame.sprite.OrderedUpdates()
        self.platforms = pygame.sprite.Group()
        self.gametime = 15
        self.hpbonus = 0
        self.speedbonus = 0
        self.scorebonus = 0

    def init_platforms(self):
        temp = []
        temp.append(Platform(*MID))
        temp.append(Platform(*LEFT))
        temp.append(Platform(*RIGHT))
        for i in range(0, len(temp)):
            self.platforms.add(temp[i])

    def on_platform(self, player):
        for platform in self.platforms:
            coll = pygame.sprite.collide_rect(platform, player)
            if coll:
                if platform.coord == MID:
                    return "mid"
                elif platform.coord == LEFT:
                    return "left"
                elif platform.coord == RIGHT:
                    return "right"
        return False

    def landed_shot(self, mob):
        for projectile in self.projectile_sprites:
            coll = pygame.sprite.collide_rect(projectile, mob)
            if coll:
                return True

        return False


    def took_damage(self, player):
        for mob in self.mob_sprites:
            coll = pygame.sprite.collide_rect(player, mob)
            if coll:
                return True

        return False

    def add_mob(self):
        num = str(random.randint(1, 5))
        loc = random.choice(['lfloor', 'rfloor', 'left', 'right'])
        hp = random.randint(10, 40) + self.hpbonus
        points = random.randint(100, 200)
        idle = Sprite("./assets/sprites/MOBS/" + num + "/Idle.png", 4, upscale=2)
        run = Sprite("./assets/sprites/MOBS/" + num + "/Run.png", 8, upscale=2)
        jump = Sprite("./assets/sprites/MOBS/" + num + "/Jump.png", 2, upscale=2)
        takehit = Sprite("./assets/sprites/MOBS/" + num + "/Take Hit.png", 4, upscale=2)
        death = Sprite("./assets/sprites/MOBS/" + num + "/Death.png", 4, upscale=2)
        ms = {"idle": idle, "run": run, "jump": jump, "takehit": takehit, "death": death}
        mob = Infected(*SPAWNDICT[loc], ms, hp, self.speedbonus, points)
        self.mobs.addmob(mob)

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
        self.projectile = Projectile()

    def init_mobs(self):
        self.mobs = Mobs()

    def set_score(self, score):
        self.score = score
