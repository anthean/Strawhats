from collections import defaultdict
from GameState import GameState
import pygame
import pygame_menu
import Menus

# Global variables for initial window settings
WIDTH = 800
HEIGHT = 600
FPS = 60


class CovidBlaster:
    def __init__(self):
        self.resolution = (WIDTH, HEIGHT)
        self.menu = defaultdict(pygame_menu.Menu)
        self.state = GameState()
        self.display = None
        self.current_menu = None

    def run(self):
        pygame.init()
        self.initialize_window()
        self.initialize_menus()
        self.current_menu = self.menu['MAIN MENU']

        while True:
            self.current_menu.mainloop(self.display, fps_limit=FPS)

    def initialize_window(self):
        self.display = pygame.display.set_mode(self.resolution, pygame.SCALED)
        self.resolution = self.display.get_size()

    def initialize_menus(self):
        main_choices = (self.play, self.high_scores, self.settings, pygame_menu.events.EXIT)
        play_choices = (self.state.set_name, self.main_menu)
        settings_choices = (self.set_resolution, self.main_menu)
        self.menu['MAIN MENU'] = Menus.create_main_menu(self.resolution, main_choices)
        self.menu['PLAY'] = Menus.create_play_menu(self.resolution, play_choices)
        self.menu['HIGH SCORES'] = Menus.create_hs_menu(self.resolution, self.main_menu)
        self.menu['SETTINGS'] = Menus.create_settings_menu(self.resolution, settings_choices)

    def main_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu['MAIN MENU']
        self.current_menu.enable()

    def play(self):
        self.current_menu.disable()
        self.state.new_game()
        self.current_menu = self.menu['PLAY']
        self.current_menu.enable()

    def high_scores(self):
        self.current_menu.disable()
        self.current_menu = self.menu['HIGH SCORES']
        self.current_menu.enable()

    def settings(self):
        self.current_menu.disable()
        self.current_menu = self.menu['SETTINGS']
        self.current_menu.enable()

    def set_resolution(self, resolution):
        self.resolution = resolution


if __name__ == '__main__':
    game = CovidBlaster()
    game.run()