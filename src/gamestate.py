import pygame
from sprite import Sprite
from player import Player
from window_settings import *


class GameState:
    def __init__(self):
        self.name = ''
        self.player = None
        self.score = 0
        self.game_over = False


    def start(self, display):
        self.score = 0
        self.game_over = False
        self.display = display
        clock = pygame.time.Clock()
        sprites = pygame.sprite.OrderedUpdates()
        bg = SCALE('./assets/sprites/STAGE/stage.png', (WIDTH, HEIGHT))
        self.display.blit(bg, (0, 0))
        surface = self.display.copy()
        while True:
            self.listen_for_exit()
            sprites = self.player.update(sprites)
            sprites.draw(self.display)
            pygame.display.update()
            sprites.clear(self.display, surface)
            clock.tick(FPS)


    def listen_for_exit(self):
        keys = pygame.key.get_pressed()
        if pygame.QUIT in pygame.event.get() or keys[pygame.K_ESCAPE]: pygame.quit()


    def set_name(self, name):
        self.name = name


    def set_player(self, pcolor, difficulty):
        idle = Sprite(pcolor+'idle.png', 5, upscale=4)
        run = Sprite(pcolor+'run.png', 6, upscale=4)
        jump = Sprite(pcolor+'jump.png', 2, upscale=4)
        crouch = Sprite(pcolor+'crouch.png', 3, upscale=4)
        death = Sprite(pcolor+'death.png', 8, upscale=4)
        ps = {'idle':idle, 'run':run, 'jump':jump, 'crouch':crouch, 'death':death}
        self.player = Player(ps, difficulty)


    def set_score(self, score):
        self.score = score
