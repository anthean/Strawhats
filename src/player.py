import pygame
from window_settings import *


class Player:
    def __init__(self, ps, difficulty):
        self.ps = ps
        self.current_sprite = self.ps['idle']
        self.immune_system = difficulty
        self.x = PX(0.5)
        self.y = PY(0.82)
        self.speed = PX(0.0045)
        self.flip = False
        self.frame = {'idle':0, 'run':0, 'jump':0, 'crouch':0, 'death':0}
        self.next_frame = pygame.time.get_ticks()

    def update(self, sprites):
        sprites.remove(self.current_sprite)
        keys = pygame.key.get_pressed()
        if self.immune_system == 0: self.death()
        elif keys[pygame.K_RIGHT]: self.run_right()
        elif keys[pygame.K_LEFT]: self.run_left()
        elif keys[pygame.K_UP]: self.jump()
        elif keys[pygame.K_DOWN]: self.crouch()
        else: self.idle()
        self.current_sprite.move(self.x, self.y, True)
        sprites.add(self.current_sprite)
        return sprites

    def idle(self):
        self.current_sprite = self.ps['idle']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['idle'] = (self.frame['idle']+1) % 5
            self.next_frame += FPS
        self.current_sprite.update_sprite(self.frame['idle'], self.flip)

    def run_right(self):
        self.flip = False
        self.current_sprite = self.ps['run']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['run'] = (self.frame['run']+1) % 6
            self.next_frame += FPS
        self.x += self.speed
        if self.x >= PX(1): self.x = PX(0)
        self.current_sprite.update_sprite(self.frame['run'], self.flip)
    
    def run_left(self):
        self.flip = True
        self.current_sprite = self.ps['run']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['run'] = (self.frame['run']+1) % 6
            self.next_frame += FPS
        self.x -= self.speed
        if self.x <= PX(0): self.x = PX(1)
        self.current_sprite.update_sprite(self.frame['run'], self.flip)
    
    def jump(self):
        self.current_sprite = self.ps['jump']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['jump'] = 1
            self.next_frame += FPS
        self.current_sprite.update_sprite(self.frame['jump'], self.flip)
        
    def crouch(self):
        self.current_sprite = self.ps['crouch']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['crouch'] += 1
            self.next_frame += FPS
        if self.frame['crouch'] > 2: self.frame['crouch'] = 2
        self.current_sprite.update_sprite(self.frame['crouch'], self.flip)
    
    def death(self):
        self.current_sprite = self.ps['death']
        if pygame.time.get_ticks() > self.next_frame:
            self.frame['death'] = (self.frame['death']+1) % 8
            self.next_frame += FPS
        self.current_sprite.update_sprite(self.frame['death'], self.flip)
