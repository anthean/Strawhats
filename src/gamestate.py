import sys
import menus
from sprite import Sprite
from player import Player
from window_settings import *


class GameState:
    def __init__(self):
        self.name = ''
        self.player = None
        self.score = 0
        self.game_over = False
        self.surface = None
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.OrderedUpdates()
        self.bg = RESIZE(SCALE2X(pygame.image.load('./assets/sprites/STAGE/stage.png'), 3), (WIDTH, HEIGHT))
        self.current_menu = None
        self.music = None

    def start(self, display):
        self.current_menu = menus.create_intro_menu(self.continue_game)
        self.pause_menu = menus.create_pause_menu((self.continue_game, self.quit_game()))
        self.score = 0
        self.game_over = False
        self.display = display
        self.display.blit(self.bg, (0, 0))
        self.surface = self.display.copy()
        self.current_menu.enable()
        while True:
            events = pygame.event.get()
            if self.current_menu.is_enabled():
                self.bgm.set_volume(0.06)
                self.current_menu.draw(self.display)
                self.current_menu.update(events)
                pygame.display.update()
                self.clock.tick(FPS)/1000.0 
            else:
                for event in events: self.handle_events(event)
                self.sprites = self.player.update(self.sprites)
                self.sprites.draw(self.display)
                pygame.display.update() 
                self.sprites.clear(self.display, self.surface)
                self.clock.tick(FPS)/1000.0


    def continue_game(self):
        self.bgm.set_volume(0.20)
        self.display.blit(self.bg, (0, 0))
        self.current_menu.disable()
        self.clock.tick(FPS)/1000.0

    def quit_game(self):
        self.current_menu.disable()

    def handle_events(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.current_menu = self.pause_menu
            self.current_menu.enable()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def set_name(self, name):
        menus.SOUND.play_event()
        self.name = name.upper()

    def set_player(self, pcolor, difficulty):
        idle = Sprite(pcolor+'idle.png', 5, upscale=2)
        run = Sprite(pcolor+'run.png', 6, upscale=2)
        jump = Sprite(pcolor+'jump.png', 2, upscale=2)
        crouch = Sprite(pcolor+'crouch.png', 3, upscale=2)
        death = Sprite(pcolor+'death.png', 8, upscale=2)
        ps = {'idle':idle, 'run':run, 'jump':jump, 'crouch':crouch, 'death':death}
        self.player = Player(ps, difficulty)

    def set_music(self, on):
        self.music = on
        self.bgm = pygame.mixer.Sound('./assets/sfx/bgm.ogg')
        self.bgm.set_volume(0.06)
        if on: self.bgm.play(-1)

    def set_score(self, score):
        self.score = score
