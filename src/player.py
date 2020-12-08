from sprite import Sprite, jforce
from window_settings import *


INIT_VELOCTIY = 30


class Player:
    def __init__(self, ps, difficulty):
        self.ps = ps
        self.immune_system = difficulty
        self.shadow = Sprite(
            "./assets/sprites/EXTRAS/shadow.png",
            1,
            upscale=2,
            resize=(PX(0.085), PY(0.1)),
        )
        self.frame = {"idle": 0, "run": 0, "jump": 0, "crouch": 0, "death": 0}
        self.current_sprite = self.ps["idle"]
        self.current_frame = 0
        self.x = PX(0.5)
        self.y = PY(0.82)
        self.speed = PX(0.0045)
        self.mass = 0.05
        self.yspeed = INIT_VELOCTIY
        self.running = False
        self.flip = False
        self.crouching = False
        self.jumping = False
        self.falling = False
        self.plat_coll = False
        self.jump_sfx = pygame.mixer.Sound("assets/sfx/game/jump.wav")
        self.clock = None
        self.next_frame = pygame.time.get_ticks()

    def get_sprite(self):
        return self.current_sprite

    def handle_events(self, event):
        self.event = event
        if (
            self.event.type == pygame.KEYDOWN
            and self.event.key == pygame.K_UP
            and not self.jumping and not self.falling
        ):
            self.jumping = True
            self.jump_sfx.play()


    def update(self, sprites):
        sprites.remove(self.current_sprite)
        self.keys = pygame.key.get_pressed()
        if self.immune_system == 0:
            self.death()
        elif self.keys[pygame.K_RIGHT]:
            self.run_right()
        elif self.keys[pygame.K_LEFT]:
            self.run_left()
        elif self.keys[pygame.K_DOWN]:
            if not self.crouching:
                self.crouch()
        else:
            self.idle()

        if self.jumping:
            self.jump()
        
        if self.falling:
            self.current_frame = self.frame['jump']
            self.fall()
        self.current_sprite.update_sprite(self.current_frame, self.flip)
        self.current_sprite.move(self.x, self.y)
        shadow_adj = -PX(0.005) if self.flip else PX(0.005)
        y_shadow = self.y + PY(0.076) if not self.jumping else PY(1) - PY(0.086)
        self.shadow.move(self.x - shadow_adj, y_shadow)
        sprites.add(self.current_sprite, self.shadow)
        return sprites

    def idle(self):
        self.crouching = False
        self.current_sprite = self.ps["idle"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["idle"] = (self.frame["idle"] + 1) % 5
            self.next_frame += FPS
        self.current_frame = self.frame["idle"]


    def run_right(self):
        self.flip = False
        if not self.jumping:
            self.current_sprite = self.ps["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 6
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x += self.speed
        if self.x >= PX(1):
            self.x = PX(0)

        if (
            self.event.type == pygame.KEYDOWN
            and self.event.key == pygame.K_UP
            and not self.jumping and not self.falling
        ):
            self.jumping = True
            self.jump_sfx.play()

    def run_left(self):
        self.flip = True
        if not self.jumping:
            self.current_sprite = self.ps["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 6
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x -= self.speed
        if self.x <= PX(0):
            self.x = PX(1)

        if (
            self.event.type == pygame.KEYDOWN
            and self.event.key == pygame.K_UP
            and not self.jumping and not self.falling
        ):
            self.jumping = True
            self.jump_sfx.play()

    def jump(self):
        self.current_sprite = self.ps["jump"]
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
        

    def crouch(self):
        self.current_sprite = self.ps["crouch"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["crouch"] = (self.frame["crouch"] + 1) % 3
            self.next_frame += FPS
        self.current_frame = self.frame["crouch"]
        if self.frame["crouch"] == 2:
            self.crouching = True

    def death(self):
        self.current_sprite = self.ps["death"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["death"] = (self.frame["death"] + 1) % 8
            self.next_frame += FPS
        self.current_frame = self.frame["death"]
