from sprite import Sprite
from window_settings import *


class Player:
    def __init__(self, ps, difficulty):
        self.ps = ps
        self.current_sprite = self.ps['idle']
        self.shadow = Sprite('./assets/sprites/EXTRAS/shadow.png', 1, upscale=2, resize=( PX(0.085), PY(0.1) ))
        self.frame = {'idle':0, 'run':0, 'jump':0, 'crouch':0, 'death':0}
        self.current_frame = self.frame['idle']
        self.immune_system = difficulty
        self.x = PX(0.5)
        self.y = PY(0.82)
        self.speed = PX(0.0045)
        self.flip = False
        self.jumping = False
        self.next_frame = pygame.time.get_ticks()

    def update(self, sprites):
        sprites.remove(self.current_sprite)
        keys = pygame.key.get_pressed()
        if self.immune_system == 0: self.death()
        if keys[pygame.K_RIGHT]: self.run_right()
        elif keys[pygame.K_LEFT]: self.run_left()
        elif keys[pygame.K_UP]: self.jump()
        elif keys[pygame.K_DOWN]: self.crouch()
        else: self.idle()
        self.current_sprite.update_sprite(self.current_frame, self.flip)
        self.current_sprite.move(self.x, self.y)
        shadow_adj = -PX(0.005) if self.flip else PX(0.005)
        self.shadow.move(self.x-shadow_adj, self.y+PY(0.076))
        sprites.add(self.current_sprite, self.shadow)
        return sprites

    def idle(self):
        self.current_sprite = self.ps['idle']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['idle'] = (self.frame['idle'] + 1) % 5
            self.next_frame += FPS
        self.current_frame = self.frame['idle']

    def run_right(self):
        self.flip = False
        self.current_sprite = self.ps['run']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['run'] = (self.frame['run'] + 1) % 6
            self.next_frame += FPS
        self.x += self.speed
        if self.x >= PX(1): self.x = PX(0)
        self.current_frame = self.frame['run']
    
    def run_left(self):
        self.flip = True
        self.current_sprite = self.ps['run']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['run'] = (self.frame['run'] + 1) % 6
            self.next_frame += FPS
        self.x -= self.speed
        if self.x <= PX(0): self.x = PX(1)
        self.current_frame = self.frame['run']
    
    def jump(self):
        self.current_sprite = self.ps['jump']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['jump'] = 1
            self.next_frame += FPS
        self.current_frame = self.frame['jump']
        
    def crouch(self):
        self.current_sprite = self.ps['crouch']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['crouch'] += 1
            self.next_frame += FPS
        if self.frame['crouch'] > 2: self.frame['crouch'] = 2
        self.current_frame = self.frame['crouch']
    
    def death(self):
        self.current_sprite = self.ps['death']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['death'] = (self.frame['death'] + 1) % 8
            self.next_frame += FPS
        self.current_frame = self.frame['death']
