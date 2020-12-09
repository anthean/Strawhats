from sprite import Sprite, jforce
from window_settings import *

INIT_VELOCTIY = 30


class Infected:
    def __init__(self, x, y, ms, hp):
        self.ms = ms
        self.hp = hp
        self.frame = {"idle": 0, "run": 0, "jump": 0, "takehit": 0, "death": 0}
        self.current_sprite = self.ms["idle"]
        self.current_frame = 0
        self.x = PX(0.5)
        self.y = PY(0.47)
        self.speed = PX(0.0045)
        self.mass = 0.05
        self.yspeed = INIT_VELOCTIY
        self.running = False
        self.flip = False
        self.crouching = False
        self.jumping = False
        self.falling = False
        self.plat_coll = False
        self.next_frame = pygame.time.get_ticks()

    def get_sprite(self):
        return self.current_sprite

    def update(self, sprites, plat_coll):
        sprites.remove(self.current_sprite)
        self.plat_coll = plat_coll
        if self.hp == 0:
            self.death()
        else:
            self.idle()

        if self.jumping:
            self.jump()

        if self.falling:
            self.current_frame = self.frame["jump"]
            self.fall()
        self.current_sprite.update_sprite(self.current_frame, self.flip)
        self.current_sprite.move(self.x, self.y)
        sprites.add(self.current_sprite)
        return sprites

    def idle(self):
        self.crouching = False
        self.current_sprite = self.ms["idle"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["idle"] = (self.frame["idle"] + 1) % 4
            self.next_frame += FPS
        self.current_frame = self.frame["idle"]

    def run_right(self):
        self.flip = False
        if not self.jumping:
            self.current_sprite = self.ms["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 8
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x += self.speed
        if self.x >= PX(1):
            self.x = PX(0)

    def run_left(self):
        self.flip = True
        if not self.jumping:
            self.current_sprite = self.ms["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 8
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x -= self.speed
        if self.x <= PX(0):
            self.x = PX(1)

    def jump(self):
        self.current_sprite = self.ms["jump"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["jump"] = 1
        self.current_frame = self.frame["jump"]
        if self.yspeed > 0:
            f = jforce(self.mass, self.yspeed)
            self.y = self.y - f
            self.yspeed = self.yspeed - 1
        else:
            self.jumping = False
            self.falling = True

    def fall(self):
        f = -jforce(self.mass, self.yspeed)
        self.y = self.y - f
        self.yspeed = self.yspeed - 1
        if self.y > PY(0.82):
            self.jump_sfx.stop()
            self.y = PY(0.82)
            self.falling = False
            self.yspeed = INIT_VELOCTIY

    def takehit(self):
        self.current_sprite = self.ms["takehit"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["takehit"] = (self.frame["takehit"] + 1) % 4
            self.next_frame += FPS
        self.current_frame = self.frame["takehit"]
        if self.frame["takehit"] == 2:
            self.crouching = True

    def death(self):
        self.current_sprite = self.ms["death"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["death"] = (self.frame["death"] + 1) % 4
            self.next_frame += FPS
        self.current_frame = self.frame["death"]
