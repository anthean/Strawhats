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
        self.is_idle = True
        self.x = PX(0.5)
        self.y = PY(0.82)
        self.speed = PX(0.0045)
        self.xspeed = PX(0.0017)
        self.yspeed = INIT_VELOCTIY
        self.mass = 0.05
        self.current_plat = "floor"
        self.running = False
        self.flip = False
        self.crouching = False
        self.jumping = False
        self.falling = False
        self.falling_from_platform = False
        self.shooting = False
        self.dead = False
        self.shot_timer = 0
        self.jump_sfx = pygame.mixer.Sound("assets/sfx/game/jump.wav")
        self.next_frame = pygame.time.get_ticks()
        self.event = pygame.event.poll()

    def get_sprite(self):
        return self.current_sprite

    def handle_events(self, event):
        self.event = event
        if self.event.type == pygame.KEYDOWN:
            if self.event.key == pygame.K_UP and not self.is_airborne():
                self.jumping = True
                self.jump_sfx.play()
            if self.event.key == pygame.K_SPACE and not self.shooting:
                self.shooting = True

    def update(self, sprites, state):
        sprites.remove(self.current_sprite)
        self.event = pygame.event.poll()
        self.keys = pygame.key.get_pressed()
        if self.immune_system == 0:
            self.death()
        elif self.keys[pygame.K_DOWN]:
            if not self.crouching:
                self.crouch()
        elif self.keys[pygame.K_RIGHT] and not self.falling_from_platform:
            self.run_right()
        elif self.keys[pygame.K_LEFT] and not self.falling_from_platform:
            self.run_left()
        else:
            self.idle()

        if self.jumping:
            self.jump()

        if self.falling:
            self.current_frame = self.frame["jump"]
            self.fall(state)

        self.update_shadow(sprites)
        self.current_sprite.update_sprite(self.current_frame, self.flip)
        self.current_sprite.move(self.x, self.y)
        sprites.add(self.current_sprite, self.shadow)
        return sprites

    def update_shadow(self, sprites):
        xshadow = -PX(0.005) if self.flip else PX(0.005)
        yshadow = self.y + PY(0.076) if not self.is_airborne() else PY(1) - PY(0.086)
        self.shadow.move(self.x - xshadow, yshadow)
        sprites.add(self.shadow)

    def idle(self):
        self.is_idle = True
        self.crouching = False
        self.running = False
        self.current_sprite = self.ps["idle"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["idle"] = (self.frame["idle"] + 1) % 5
            self.next_frame += FPS
        self.current_frame = self.frame["idle"]

    def run_right(self):
        self.is_idle = False
        self.flip = False
        self.running = True
        if not self.jumping:
            self.current_sprite = self.ps["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 6
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x += self.speed
        if self.x > PX(1):
            self.x = PX(0)
            if self.current_plat == "right":
                self.current_plat = "left"

        if not self.jumping:
            if self.current_plat == "left" and self.x > PX(0.37):
                self.yspeed = 20
                self.jumping = True
                self.falling_from_platform = True
            elif self.current_plat == "mid" and self.x > PX(0.61):
                self.yspeed = 20
                self.jumping = True
                self.falling_from_platform = True

    def run_left(self):
        self.is_idle = False
        self.flip = True
        self.running = True
        if not self.jumping:
            self.current_sprite = self.ps["run"]
            if pygame.time.get_ticks() > self.next_frame:
                self.frame["run"] = (self.frame["run"] + 1) % 6
                self.next_frame += FPS
            self.current_frame = self.frame["run"]
        self.x -= self.speed
        if self.x < PX(0):
            self.x = PX(1)
            if self.current_plat == "left":
                self.current_plat = "right"

        if not self.jumping:
            if self.current_plat == "right" and self.x < PX(0.63):
                self.yspeed = 20
                self.jumping = True
                self.falling_from_platform = True
            elif self.current_plat == "mid" and self.x < PX(0.39):
                self.yspeed = 20
                self.jumping = True
                self.falling_from_platform = True

    def shoot(self):
        if self.shooting:
            xflash = -PX(0.06) if self.flip else PX(0.06)
            if self.crouching:
                yflash = -PY(0.01)
            elif self.is_idle:
                yflash = PY(0.01)
            else:
                yflash = PY(0.025)
            if self.shot_timer == 0:
                update_params = (0, self.flip)
                move_params = (self.x + xflash, self.y - yflash)
                self.shot_timer = 12
                return (update_params, move_params)
            else:
                self.shot_timer = self.shot_timer - 1
                if self.shot_timer <= 0:
                    self.shooting = False

        return False

    def jump(self):
        self.is_idle = False
        self.running = False
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

    def fall(self, state):
        self.is_idle = False
        f = -jforce(self.mass, self.yspeed)
        self.y = self.y - f
        self.yspeed = self.yspeed - 1
        if self.falling_from_platform:
            self.x = self.x - self.xspeed if self.flip else self.x + self.xspeed
        if (
            state.on_platform(self.current_sprite) == "left"
            or state.on_platform(self.current_sprite) == "right"
        ) and self.y > PY(0.222):
            self.jump_sfx.stop()
            self.y = PY(0.222)
            self.falling = False
            self.falling_from_platform = False
            self.yspeed = INIT_VELOCTIY
            self.current_plat = state.on_platform(self.current_sprite)
        elif state.on_platform(self.current_sprite) == "mid" and self.y > PY(0.472):
            self.jump_sfx.stop()
            self.y = PY(0.472)
            self.falling = False
            self.falling_from_platform = False
            self.yspeed = INIT_VELOCTIY
            self.current_plat = "mid"
        elif self.y > PY(0.82):
            self.jump_sfx.stop()
            self.y = PY(0.82)
            self.falling = False
            self.falling_from_platform = False
            self.yspeed = INIT_VELOCTIY
            self.current_plat = "floor"

    def is_airborne(self):
        return self.jumping or self.falling

    def crouch(self):
        self.is_idle = False
        self.current_sprite = self.ps["crouch"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["crouch"] = (self.frame["crouch"] + 1) % 3
            self.next_frame += FPS
        self.current_frame = self.frame["crouch"]
        if self.frame["crouch"] == 2:
            self.crouching = True

    def death(self):
        pygame.mixer.load(GAMEOVER)
        pygame.mixer.play()
        self.current_sprite = self.ps["death"]
        if pygame.time.get_ticks() > self.next_frame:
            self.frame["death"] = (self.frame["death"] + 1) % 8
            self.next_frame += FPS
        self.current_frame = self.frame["death"]
        if self.current_frame == 7:
            self.dead = True

    def isdead(self):
        return self.dead
