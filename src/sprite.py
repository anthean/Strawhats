import pygame
from window_settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, file, count=1, upscale=0):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(file).convert_alpha()
        for _ in range(int(upscale/2)): img = SCALE2X(img)
        self.w = img.get_width() // count
        self.h = img.get_height()
        self.spritesheet = []
        self.load_sprite_sheet(img, count)
        self.image = pygame.Surface.copy(self.spritesheet[0])
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.mask = pygame.mask.from_surface(self.image)

    def load_sprite_sheet(self, img, count):
        frame = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        x = 0
        for _ in range(count):
            frame = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
            frame.blit(img, (x, 0))
            self.spritesheet.append(frame.copy())
            x -= self.w

    def move(self, xpos, ypos, center=True):
        if center: self.rect.center = [xpos, ypos]
        else: self.rect.topleft = [xpos, ypos]

    def update_sprite(self, index):
        self.image = self.spritesheet[index]
        self.rect = self.image.get_rect()
        self.w = self.rect.width
        self.h = self.rect.height
        self.mask = pygame.mask.from_surface(self.image)
