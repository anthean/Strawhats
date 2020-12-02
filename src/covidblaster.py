import pygame
import pygame_menu
import menus


from collections import namedtuple
from gamestate import GameState
from sprite import Sprite
from window_settings import *


class CovidBlaster:
    def __init__(self):
        self.state = GameState()
        self.fs = FULLSCREEN
        self.pcolor = './assets/sprites/CHARACTER_SPRITES/Red/'
        self.difficulty = 3
        self.running_preview = False
        self.music = True
        self.bgm = pygame.mixer.Sound('./assets/sfx/menubgm.ogg')
        self.display = None
        self.menu = None
        self.current_menu = None
        self.high_scores = None
        self.close_menu = False

    # Runs the game
    def run(self):
        self.initialize_window()
        self.initialize_menus()
        self.get_high_scores()
        while True: self.current_menu.mainloop(self.display)

    # Plays the game
    def play(self):
        self.bgm.stop()
        self.running_preview = False
        self.current_menu.disable()
        self.state.set_player(self.pcolor, self.difficulty)
        self.state.start(self.display)


    # Initializes the window
    def initialize_window(self):
        pygame.init()
        if FULLSCREEN: self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED | pygame.FULLSCREEN)
        else: self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
        pygame.display.set_caption('COVIDBLASTER')
        pygame.display.set_icon(RESIZE('./assets/sprites/CHARACTER_SPRITES/Black/icon.png', (64, 64)))


    # Creation of pygame_menu menu objects with functions defined in menus.py
    def initialize_menus(self):
        main_choices = (self.set_play_menu, self.set_high_scores_menu, self.set_settings_menu, pygame_menu.events.EXIT)
        self.play_choices = (self.state.set_name, self.set_player_color, self.set_difficulty, self.play, self.set_main_menu)
        settings_choices = (self.toggle_fs, self.toggle_music, self.set_confirmation_menu, self.set_main_menu)
        confirmation_choices = (self.clear_high_scores, self.set_settings_menu)
        Menu = namedtuple('Menu', ['main_menu', 'play', 'high_scores', 'settings', 'confirmation'])
        main_menu = menus.create_main_menu(main_choices)
        play = menus.create_play_menu(self.play_choices)
        high_scores = pygame_menu.Menu(HEIGHT, WIDTH, 'HIGH SCORES', theme=menus.THEME)
        settings = menus.create_settings_menu(settings_choices)
        confirmation = menus.create_confirmation_menu(confirmation_choices)
        self.menu = Menu(main_menu, play, high_scores, settings, confirmation)
        self.current_menu = self.menu.main_menu
        self.bgm.set_volume(0.25)
        self.bgm.play(-1)


    # Sets the current menu to the main menu
    def set_main_menu(self):
        self.running_preview = False
        menus.SOUND.play_close_menu()
        self.current_menu.disable()
        self.current_menu = self.menu.main_menu
        self.current_menu.enable()


    # Sets the current menu to the play menu and the game state to a new game
    def set_play_menu(self):
        self.current_menu.disable()
        self.current_menu = menus.create_play_menu(self.play_choices)
        self.state = GameState()
        self.current_menu.enable()
        self.preview_color('./assets/sprites/CHARACTER_SPRITES/Red/')

    # Used to set the player color in the play menu
    def set_player_color(self, _, path):
        menus.SOUND.play_event()
        self.pcolor = path
        self.preview_color(path)

    def preview_color(self, path):
        clock = pygame.time.Clock()
        next_frame = pygame.time.get_ticks()
        frame = 0
        preview = Sprite(path+'idle.png', 5, upscale=2)
        sprites = pygame.sprite.OrderedUpdates()
        surface = self.display.copy()
        self.running_preview = True
        while self.running_preview:
            sprites.add(preview)
            events = pygame.event.get()
            self.current_menu.update(events)
            self.current_menu.draw(self.display)
            if pygame.time.get_ticks() > next_frame:
                frame = (frame + 1) % 5
                next_frame += FPS
            preview.update_sprite(frame)
            preview.move(PX(0.5), PY(0.35), center=True)
            sprites.draw(self.display)
            pygame.display.update()
            sprites.clear(self.display, surface)
            clock.tick(FPS)

    # Used to set the difficulty in the play menu
    def set_difficulty(self, _, difficulty):
        menus.SOUND.play_event()
        self.difficulty = difficulty


    # Sets the current menu to the high score menu
    def set_high_scores_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.high_scores
        self.current_menu.clear()

        for score in self.high_scores:
            name, value = score.strip().split(':')
            self.current_menu.add_label(f'{name:<15}{value:>15}')
        
        for _ in range(10-len(self.high_scores)): self.current_menu.add_label('')
        self.current_menu.add_button('BACK', self.set_main_menu)
        self.current_menu.set_sound(menus.SOUND)
        self.current_menu.enable()

    # Gets the high scores from the text file and stores it in a list
    def get_high_scores(self):
        with open('high_scores.txt') as f: self.high_scores = f.readlines()
        self.high_scores.sort(key=lambda score: int(score.split(':')[1].strip()), reverse=True)


    # Sets the current menu to the settings menu
    def set_settings_menu(self):
        if self.close_menu: menus.SOUND.play_close_menu()
        self.close_menu = False
        self.current_menu.disable()
        self.current_menu = self.menu.settings
        self.current_menu.enable()

    # Toggle between fs and windowed
    def toggle_fs(self, _, __):
        menus.SOUND.play_event()
        if self.fs:
            self.set_windowed()
            self.fs = False
        else:
            self.set_fs()
            self.fs = True

    def set_fs(self):
        self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED | pygame.FULLSCREEN)

    def set_windowed(self):
        pygame.display.toggle_fullscreen()
        self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)

    # Toggle music
    def toggle_music(self, _, __):
        menus.SOUND.play_event()
        if self.music:
            self.bgm.set_volume(0)
            self.music = False
        else:
            self.bgm.set_volume(0.25)
            self.music = True 

    # Clears the high scores
    def clear_high_scores(self):
        self.close_menu = False
        menus.SOUND.play_error()
        with open('high_scores.txt', 'w') as f: f.truncate(0)
        self.high_scores = []
        self.set_settings_menu()

    # Confirmation menu for deleting high scores
    def set_confirmation_menu(self):
        self.close_menu = True
        self.current_menu.disable()
        self.current_menu = self.menu.confirmation
        self.current_menu.enable()


if __name__ == '__main__':
    game = CovidBlaster()
    game.run()
