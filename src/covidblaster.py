import pygame
import pygame_menu
import pygameextra as pe
import menus

from collections import namedtuple
from gamestate import GameState
from player import Player
from infected import Infected


# Global variables for initial window settings
WIDTH = 800
HEIGHT = 600
FPS = 60


# Lambda shortcuts
load_image = lambda path, dimensions: pygame.transform.scale(pygame.image.load(path), dimensions)
to_pixel = lambda frac: (frac[0]*WIDTH, frac[1]*HEIGHT)


class CovidBlaster:
    def __init__(self):
        self.resolution = (WIDTH, HEIGHT)
        self.state = GameState()
        self.display = None
        self.menu = None
        self.sprites = None
        self.pcolor = None
        self.psprites = None
        self.current_menu = None
        self.audio_engine = None
        self.high_scores = None

    # Runs the game
    def run(self):
        pygame.init()
        self.initialize_window()
        self.initialize_menus()
        self.initialize_audio()
        self.load_sprites()
        self.get_high_scores()

        while True:
            events = pe.event.get()
            if self.current_menu.is_enabled(): self.current_menu.update(events)
            if self.current_menu.is_enabled(): self.current_menu.draw(self.display)            
            pe.display.update()
            pe.time.tick(FPS)

    # Plays the game
    def play(self):
        self.current_menu.disable()
        
        while True:
            for pe.event.c in pe.event.get():
                pe.event.quitcheckauto()

            pe.display.update()
            pe.time.tick(FPS)

    # Initializes the window
    def initialize_window(self):
        self.display = pe.display.make(self.resolution, 'COVIDBLASTER')
        self.resolution = self.display.get_size()

    # Creation of pygame_menu menu objects with functions defined in menus.py
    def initialize_menus(self):
        main_choices = (self.set_play_menu, self.set_high_scores_menu, self.set_settings_menu, pygame_menu.events.EXIT)
        play_choices = (self.set_player_color, self.state.set_name, self.play, self.set_main_menu)
        settings_choices = (self.set_confirmation_menu, self.set_main_menu)
        confirmation_choices = (self.clear_high_scores, self.set_settings_menu)
        Menu = namedtuple('Menu', ['main_menu', 'play', 'high_scores', 'settings', 'confirmation'])
        main_menu = menus.create_main_menu(self.resolution, main_choices)
        play = menus.create_play_menu(self.resolution, play_choices)
        high_scores = menus.create_hs_menu(self.resolution, self.set_main_menu)
        settings = menus.create_settings_menu(self.resolution, settings_choices)
        confirmation = menus.create_confirmation_menu(self.resolution, confirmation_choices)
        self.menu = Menu(main_menu, play, high_scores, settings, confirmation)
        self.current_menu = self.menu.main_menu

    # Initializes the audio engine
    def initialize_audio(self):
        self.audio_engine = pygame_menu.sound.Sound()
        self.audio_engine.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, './assets/sfx/confirm.wav')
        self.audio_engine.set_sound(pygame_menu.sound.SOUND_TYPE_OPEN_MENU, './assets/sfx/confirm.wav')
        self.audio_engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLOSE_MENU, './assets/sfx/confirm.wav')
        self.audio_engine.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_ADDITION, './assets/sfx/confirm.wav')
        self.audio_engine.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_DELETION, './assets/sfx/confirm.wav')
        self.current_menu.set_sound(self.audio_engine)

    # Loads the sprites
    def load_sprites(self):
        Sprites = namedtuple('Sprites', ['layer0', 'layer1', 'layer2', 'layer3', 'platform', 'bulletstream', 'muzzleflash'])
        layer0 = load_image('./assets/sprites/ENVIRONMENT/bg-0.png', self.resolution).convert()
        layer1 = load_image('./assets/sprites/ENVIRONMENT/bg-1.png', self.resolution).convert()
        layer2 = load_image('./assets/sprites/ENVIRONMENT/bg-2.png', self.resolution).convert()
        layer3 = load_image('./assets/sprites/ENVIRONMENT/bg-3.png', self.resolution).convert()
        platform = load_image('./assets/sprites/ENVIRONMENT/platform.png', self.resolution).convert()
        bulletstream = load_image('./assets/sprites/EXTRAS/BulletStream.png', self.resolution).convert()
        muzzleflash = load_image('./assets/sprites/EXTRAS/MuzzleFlash.png', self.resolution).convert()
        self.sprites = Sprites(layer0, layer1, layer2, layer3, platform, bulletstream, muzzleflash)

    # Loads the player sprites
    def load_player_sprites(self):
        PlayerSprites = namedtuple('PlayerSprites', ['idle', 'run', 'jump', 'death'])
        idle = load_image(self.pcolor+'idle.png', self.resolution).convert()
        run = load_image(self.pcolor+'run.png', self.resolution).convert()
        jump = load_image(self.pcolor+'jump.png', self.resolution).convert()
        death = load_image(self.pcolor+'death.png', self.resolution).convert()
        self.psprites = PlayerSprites(idle, run, jump, death)

    # Sets the current menu to the main menu
    def set_main_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.main_menu
        self.current_menu.set_sound(self.audio_engine)
        self.current_menu.enable()

    # Sets the current menu to the play menu and the game state to a new game
    def set_play_menu(self):
        self.current_menu.disable()
        self.state.new_game()
        self.current_menu = self.menu.play
        self.current_menu.set_sound(self.audio_engine)
        self.current_menu.enable()

    # Used to set the player color in the play menu
    def set_player_color(self, _, path):
        self.pcolor = path 

    # Sets the current menu to the high score menu
    def set_high_scores_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.high_scores
        self.current_menu.set_sound(self.audio_engine)
        self.current_menu.clear()

        for score in self.high_scores:
            name, value = score.strip().split(':')
            self.current_menu.add_label(f'{name:<30}{value:>30}')

        self.current_menu.add_button('BACK', self.set_main_menu)
        self.current_menu.enable()

    # Gets the high scores from the text file and stores it in a list
    def get_high_scores(self):
        with open('high_scores.txt') as f: self.high_scores = f.readlines()
        self.high_scores.sort(key=lambda score: int(score.split(':')[1].strip()), reverse=True)

    # Sets the current menu to the settings menu
    def set_settings_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.settings
        self.current_menu.set_sound(self.audio_engine)
        self.current_menu.enable()

    # Confirmation menu for deleting high scores
    def set_confirmation_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.confirmation
        self.current_menu.set_sound(self.audio_engine)
        self.current_menu.enable()

    # Clears the high scores
    def clear_high_scores(self):
        with open('high_scores.txt', 'w') as f: f.truncate(0)
        self.high_scores = []
        self.set_settings_menu()


if __name__ == '__main__':
    game = CovidBlaster()
    game.run()