from collections import namedtuple
from gamestate import GameState
from player import Player
from infected import Infected
import pygame
import pygame_menu
import menus


# Global variables for initial window settings
WIDTH = 800
HEIGHT = 600
FPS = 60


class CovidBlaster:
    def __init__(self):
        self.resolution = (WIDTH, HEIGHT)
        self.state = GameState()
        self.display = None
        self.menu = None
        self.current_menu = None
        self.audio_engine = None

    # Runs the game
    def run(self):
        pygame.init()
        self.initialize_window()
        self.initialize_menus()
        self.initialize_audio()

        while True:
            self.current_menu.mainloop(self.display, fps_limit=FPS)

    # Initializes the window
    def initialize_window(self):
        self.display = pygame.display.set_mode(self.resolution, pygame.SCALED)
        self.resolution = self.display.get_size()

    # Creation of pygame_menu menu objects with functions defined in menus.py
    def initialize_menus(self):
        main_choices = (self.set_play_menu, self.set_high_scores_menu, self.set_settings_menu, pygame_menu.events.EXIT)
        play_choices = (self.state.set_name, self.set_main_menu)
        settings_choices = (self.set_resolution, self.set_main_menu)
        Menu = namedtuple('Menu', ['main_menu', 'play', 'high_scores', 'settings'])
        main_menu = menus.create_main_menu(self.resolution, main_choices)
        play = menus.create_play_menu(self.resolution, play_choices)
        high_scores = menus.create_hs_menu(self.resolution, self.set_main_menu)
        settings = menus.create_settings_menu(self.resolution, settings_choices)
        self.menu = Menu(main_menu, play, high_scores, settings)
        self.current_menu = self.menu.main_menu

    # Initializes the audio engine
    def initialize_audio(self):
        self.audio_engine = pygame_menu.sound.Sound()
        self.audio_engine.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, './assets/sfx/confirm.wav')
        self.current_menu.set_sound(self.audio_engine)

    # Sets the current menu to the main menu
    def set_main_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.main_menu
        self.current_menu.enable()

    # Sets the current menu to the play menu and the game state to a new game
    def set_play_menu(self):
        self.current_menu.disable()
        self.state.new_game()
        self.current_menu = self.menu.play
        self.current_menu.enable()

    # Sets the current menu to the high score menu
    def set_high_scores_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.high_scores
        self.current_menu.enable()

    # Sets the current menu to the settings menu
    def set_settings_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.settings
        self.current_menu.enable()

    # Sets the current resolution to the one being passed in
    def set_resolution(self, resolution: tuple):
        self.resolution = resolution


if __name__ == '__main__':
    game = CovidBlaster()
    game.run()