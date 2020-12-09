from math import sqrt

from window_settings import *

jforce = lambda mass, velocity: 0.5 * mass * (velocity ** 2)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, file, frames=1, upscale=0, resize=False):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(file).convert_alpha()
        img = SCALE2X(img, upscale)
        if resize:
            img = RESIZE(img, resize)
        self.w = img.get_width() // frames
        self.h = img.get_height()
        self.spritesheet = []
        self.load_sprite_sheet(img, frames)
        self.image = pygame.Surface.copy(self.spritesheet[0])
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.mask = pygame.mask.from_surface(self.image)

    def load_sprite_sheet(self, img, frames):
        frame = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        x = 0
        for _ in range(frames):
            frame = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
            frame.blit(img, (x, 0))
            self.spritesheet.append(frame.copy())
            x -= self.w

    def move(self, xpos, ypos=False, center=True):
        if not ypos:
            xpos = self.rect.center[0] + xpos
            ypos = self.rect.center[1]
        if center:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def update_sprite(self, index, flip=False):
        self.image = FLIP(self.spritesheet[index]) if flip else self.spritesheet[index]
        self.rect = self.image.get_rect()
        self.w = self.rect.width
        self.h = self.rect.height
        self.mask = pygame.mask.from_surface(self.image)
        self.flip = flip
