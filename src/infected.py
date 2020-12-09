from sprite import Sprite, jforce
from window_settings import *

INIT_SPEED = 30

class Infected:
    def __init__(self, x, y, ms, hp, speedbonus, points):
        self.shadow = Sprite(
            "./assets/sprites/EXTRAS/shadow.png",
            1,
            upscale=2,
            resize=(PX(0.085), PY(0.1)),
        )
        self.bulletsponge = Sprite(
            "./assets/sprites/EXTRAS/SpongeBullet.png",
            1,
            upscale=2)
        if (x, y) == ((-PX(0.75)), (PY(0.222))):
            self.current_plat = 'left'
        elif (x, y) == ((PX(1.25)), (PY(0.222))):
            self.current_plat = 'right'
        else:
            self.current_plat = 'floor'

        self.ms = ms
        self.hp = hp
        self.frame = {"idle": 0, "run": 0, "jump": 0, "takehit": 0, "death": 0}
        self.current_sprite = self.ms["idle"]
        self.current_frame = 0
        self.x = x
        self.y = y
        self.speed = PX(0.0045) + speedbonus
        self.xspeed = PX(0.0017)
        self.yspeed = INIT_SPEED
        self.mass = 0.05
        self.flip = False
        self.jumping = False
        self.falling = False
        self.takinghit = False        
        self.dead = False
        self.dying = False
        self.points = points
        self.action_counter = 0
        self.current_action = 'none'
        self.next_frame = pygame.time.get_ticks()

    def get_sprite(self):
        return self.current_sprite

    def update(self, sprites, state, player, pplat):
        sprites.remove(self.current_sprite, self.shadow)
        landed_shots = state.landed_shot(self.current_sprite)
        if self.hp <= 0:
            self.death()

        elif (landed_shots or self.takinghit) and self.hp > 0:
            self.hp -= 1
            self.takinghit = True
            self.takehit()

        else:
            px = player.rect.center[0]
            py = player.rect.center[1]

            totheleft = True if self.x > px else False
            totheright = True if not totheleft else False
            isabove = True if (pplat == 'left' or pplat == 'right') and self.current_plat == 'floor' else False
            isbelow = True if not isabove else False
            if not self.isdead():
                if self.hp <= 0:
                    self.death()
                elif self.x > PX(0.37) and self.current_plat == 'left':
                    self.run_left()
                elif self.x < PX(0.63) and self.current_plat == 'right':
                    self.run_right()
                elif self.action_counter == 0:
                    self.action_counter = 300
                    if pplat == 'mid' and self.current_plat == 'floor' and (PX(0.418) < self.x < PX(0.582)):
                        self.jumping = True
                        if totheright:
                            self.run_right()
                        elif totheleft:
                            self.run_left()
                    elif pplat == 'left' and self.current_plat == 'floor' and self.x > PX(0.9):
                        self.run_right()
                    elif pplat == 'right' and self.current_plat == 'floor' and self.x < PX(0.1):
                        self.run_left()
                    elif totheright:
                        self.run_right()
                    elif totheleft:
                        self.run_left()
                    else:
                        self.idle()
                else:
                    if pplat == 'mid' and self.current_plat == 'floor' and (PX(0.418) < self.x < PX(0.582)):
                        self.jumping = True
                    if self.current_action == 'runleft':
                        if self.x < PX(0.63) and self.current_plat == 'right':
                            self.run_right()
                        else:
                            self.run_left()
                    elif self.current_action == 'runright':
                        if self.x > PX(0.37) and self.current_plat == 'left':
                            self.run_left()
                        self.run_right()
                    elif self.current_action == 'idle':
                        self.idle()
                    self.action_counter -= 1

        if self.jumping and not landed_shots:
            self.jump()

        if self.falling and not landed_shots:
            self.current_frame = self.frame["jump"]
            self.fall()

        self.update_shadow(sprites)
        self.current_sprite.update_sprite(self.current_frame, self.flip)
        self.current_sprite.move(self.x, self.y)

        if not self.isdead():
            sprites.add(self.current_sprite, self.shadow)
        else:
            sprites.remove(self.current_sprite, self.shadow)

        return sprites

    def update_shadow(self, sprites):
        yshadow = self.y + PY(0.076) if not self.is_airborne() else PY(1) - PY(0.086)
        self.shadow.move(self.x, yshadow)
        sprites.add(self.shadow)

    def idle(self):
        self.current_action = 'idle'
        self.crouching = False
        self.current_sprite = self.ms["idle"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["idle"] = (self.frame["idle"] + 1) % 4
            self.next_frame += FPS
        self.current_frame = self.frame["idle"]

    def run_right(self):
        self.current_action = 'runright'
        self.flip = False
        if not self.jumping:
            self.current_sprite = self.ms["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 8
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x += self.speed

        if self.x > PX(1):
            if self.current_plat == 'right':
                self.current_plat = 'floor'
                self.y = PY(0.82)
            elif self.current_plat == 'floor':
                self.current_plat = 'left'
                self.y = PY(0.222)
            self.x = PX(0)

        if self.jumping:
            self.jump()


    def run_left(self):
        self.current_action = 'runleft'
        self.flip = True
        if not self.jumping:
            self.current_sprite = self.ms["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 8
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x -= self.speed

        if self.x < PX(0):
            if self.current_plat == 'left':
                self.current_plat = 'floor'
                self.y = PY(0.82)
            elif self.current_plat == 'floor':
                self.current_plat = 'right'
                self.y = PY(0.222)
            self.x = PX(1)

        if self.jumping:
            self.jump()

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
            self.y = PY(0.82)
            self.falling = False
            self.yspeed = INIT_SPEED
            self.current_plat = "floor"

    def is_airborne(self):
        return self.jumping or self.falling

    def takehit(self):
        self.current_sprite = self.ms["takehit"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["takehit"] = (self.frame["takehit"] + 1) % 4
            self.next_frame += FPS
        self.current_frame = self.frame["takehit"]
        if self.current_frame == 3:
            self.takinghit = False

    def death(self):
        if not self.dead:
            self.current_sprite = self.ms["death"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["death"] = (self.frame["death"] + 1) % 4
                self.next_frame += FPS
            self.current_frame = self.frame["death"]
        if self.frame["death"] == 3:
            self.dead = True


    def isdead(self):
        return self.dead
