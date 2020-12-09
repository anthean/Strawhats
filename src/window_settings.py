import getpass
import sys

import pygame

pygame.init()

# Global variables for initial window settings
FPS = 60
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = True
BGM = "./assets/sfx/bgm.ogg"
MBGM = "./assets/sfx/menubgm.ogg"
GAMEOVER = "./assets/sfx/game/gameover.wav"


# Utility Functions
PX = lambda x: int(x * WIDTH)
PY = lambda y: int(y * HEIGHT)
FLIP = lambda img: pygame.transform.flip(img, True, False)
R = lambda left, top, width, height: pygame.Rect(
    PX(left), PY(top), PX(width), PY(height)
)


def RESIZE(file, dim):
    if isinstance(file, str):
        return pygame.transform.smoothscale(
            pygame.image.load(file).convert_alpha(), dim
        )
    else:
        return pygame.transform.smoothscale(file, dim)


def SCALE2X(img, x):
    for _ in range(x):
        img = pygame.transform.scale2x(img)
    return img


BG = RESIZE(
    SCALE2X(pygame.image.load("./assets/sprites/STAGE/stage.png"), 3), (WIDTH, HEIGHT)
)

H = PY(0.01)
MID = (PX(0.49), PY(0.43), PX(0.02), H)
LEFT = (PX(0.28), PY(0.17), PX(0.02), H)
RIGHT = (PX(0.7), PY(0.17), PX(0.02), H)
