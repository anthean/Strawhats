import pygame
import pygame_menu
import menus


from collections import namedtuple
from gamestate import GameState
from window_settings import *


class CovidBlaster:
    def __init__(self):
        self.state = GameState()
        self.pcolor = './assets/sprites/CHARACTER_SPRITES/Red/'
        self.toggle = FULLSCREEN
        self.difficulty = 3
        self.display = None
        self.menu = None
        self.current_menu = None
        self.audio_engine = None
        self.high_scores = None


    # Runs the game
    def run(self):
        pygame.init()
        self.initialize_window()
        self.initialize_menus()
        self.initialize_audio()
        self.get_high_scores()
        while True: self.current_menu.mainloop(self.display, fps_limit=FPS)


    # Plays the game
    def play(self):
        self.current_menu.disable()
        self.state.set_player(self.pcolor, self.difficulty)
        self.state.start(self.display)


    # Used to set the player color in the play menu
    def set_player_color(self, _, path):
        self.pcolor = path 


    # Used to set the difficulty in the play menu
    def set_difficulty(self, _, difficulty):
        self.difficulty = difficulty


    # Initializes the window
    def initialize_window(self):
        pygame.init()
        if FULLSCREEN: self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED | pygame.FULLSCREEN)
        else: self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
        pygame.display.set_caption('COVIDBLASTER')
        pygame.display.set_icon(RESIZE('./assets/sprites/CHARACTER_SPRITES/Black/icon.png', (64, 64)))


    # Toggle between fs and windowed
    def toggle_fs(self, _, __):
        if self.toggle:
            self.set_windowed()
            self.toggle = False
        else:
            self.set_fs()
            self.toggle = True


    def set_fs(self):
        self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED | pygame.FULLSCREEN)


    def set_windowed(self):
        pygame.display.toggle_fullscreen()
        self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)


    # Creation of pygame_menu menu objects with functions defined in menus.py
    def initialize_menus(self):
        main_choices = (self.set_play_menu, self.set_high_scores_menu, self.set_settings_menu, pygame_menu.events.EXIT)
        self.play_choices = (self.state.set_name, self.set_player_color, self.set_difficulty, self.play, self.set_main_menu)
        settings_choices = (self.toggle_fs, self.set_confirmation_menu, self.set_main_menu)
        confirmation_choices = (self.clear_high_scores, self.set_settings_menu)
        Menu = namedtuple('Menu', ['main_menu', 'play', 'high_scores', 'settings', 'confirmation'])
        main_menu = menus.create_main_menu(main_choices)
        play = menus.create_play_menu(self.play_choices)
        high_scores = menus.create_hs_menu(self.set_main_menu)
        settings = menus.create_settings_menu(settings_choices)
        confirmation = menus.create_confirmation_menu(confirmation_choices)
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


    # Sets the current menu to the main menu
    def set_main_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.main_menu
        self.current_menu.set_sound(self.audio_engine)
        self.current_menu.enable()


    # Sets the current menu to the play menu and the game state to a new game
    def set_play_menu(self):
        self.current_menu.disable()
        self.current_menu = menus.create_play_menu(self.play_choices)
        self.current_menu.set_sound(self.audio_engine)
        self.current_menu.enable()
        self.state = GameState()


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
