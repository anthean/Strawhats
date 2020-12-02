import pygame
pygame.init()


# Global variables for initial window settings
FPS = 60
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False


# Utility Functions
PX = lambda x: int(x * WIDTH)
PY = lambda y: int(y * HEIGHT)
FLIP = lambda img: pygame.transform.flip(img, True, False)

def RESIZE(file, dim):
    if isinstance(file, str): return pygame.transform.smoothscale(pygame.image.load(file).convert_alpha(), dim)
    else: return pygame.transform.smoothscale(file, dim)

def SCALE2X(img, x):
    for _ in range(x):
        img = pygame.transform.scale2x(img)
    return img
