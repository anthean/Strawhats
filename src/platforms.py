from window_settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, top, left, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.coord = (top, left, w, h)
        self.rect = pygame.Rect(top, left, w, h)
        # self.image = pygame.Surface([w, h])
        # self.image.fill(pygame.Color(255, 255, 255))
