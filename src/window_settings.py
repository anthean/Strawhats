import pygame


# Global variables for initial window settings
FPS = 60
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False


# Utility Lambdas
PX = lambda x: int(x * WIDTH)
PY = lambda y: int(y * HEIGHT)
SCALE = lambda file, dim: pygame.transform.smoothscale(pygame.image.load(file).convert_alpha(), dim)
SCALE2X = lambda img:  pygame.transform.scale2x(img)