from collections import namedtuple
from copy import deepcopy

import pygame_menu

import menus
from gamestate import GameState
from sprite import Sprite
from window_settings import *


class CovidBlaster:
    def __init__(self):
        self.state = GameState()
        self.fs = FULLSCREEN
        self.display = None
        self.menu = None
        self.current_menu = None
        self.high_scores = None
        self.pcolor = "./assets/sprites/CHARACTER_SPRITES/Red/"
        self.running_preview = False
        self.music = True
        self.back_sfx = False
        self.paused = False

    # Runs the game
    def run(self):
        self.init_window()
        self.init_menus()
        self.get_high_scores()
        pygame.mixer.music.load(MBGM)
        pygame.mixer.music.play(-1)
        while True:
            self.current_menu.mainloop(self.display)

    def play_game(self):
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            if (
                clock.tick(FPS)
                and not self.current_menu.is_enabled()
                and not self.paused
            ):
                for event in pygame.event.get():
                    self.handle_events(event)
                    self.state.player.handle_events(event)
                self.state.sprites = self.state.player.update(self.state.sprites)
                self.state.sprites.draw(self.display)
                pygame.display.update()
                self.state.sprites.clear(self.display, self.surface)
            else:
                self.current_menu.update(events)
                self.current_menu.draw(self.display)
                pygame.display.update()

    def handle_events(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.toggle_pause()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Initializes the game
    def init_game(self):
        self.running_preview = False
        self.paused = True
        self.state.set_player(self.pcolor)
        self.current_menu.disable()
        self.current_menu = self.menu.intro
        self.display.blit(BG, (0, 0))
        self.surface = self.display.copy()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(BGM)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        if not self.music:
            pygame.mixer.music.pause()

        self.current_menu.enable()

    # Initializes the window
    def init_window(self):
        pygame.init()
        if FULLSCREEN:
            self.display = pygame.display.set_mode(
                [WIDTH, HEIGHT], pygame.SCALED | pygame.FULLSCREEN
            )
        else:
            self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
            pygame.display.set_caption("COVIDBLASTER")
            pygame.display.set_icon(
                RESIZE("./assets/sprites/EXTRAS/icon.png", (64, 64))
            )

            # self.clock = pygame.time.Clock()

    # Creation of pygame_menu menu objects with functions defined in menus.py
    def init_menus(self):
        main_choices = (
            self.set_play_menu,
            self.set_high_scores_menu,
            self.set_settings_menu,
            pygame_menu.events.EXIT,
        )
        self.play_choices = (
            self.state.set_name,
            self.set_player_color,
            self.set_difficulty,
            self.init_game,
            self.set_main_menu,
        )
        settings_choices = (
            self.toggle_fs,
            self.toggle_music,
            self.set_confirmation_menu,
            self.set_main_menu,
        )
        confirmation_choices = (self.clear_high_scores, self.set_settings_menu)
        pause_choices = (self.toggle_pause, self.set_main_menu)
        Menu = namedtuple(
            "Menu",
            ["main_menu", "high_scores", "settings", "confirmation", "intro", "pause"],
        )
        main_menu = menus.create_main_menu(main_choices)
        high_scores = pygame_menu.Menu(
            HEIGHT, WIDTH, "HIGH SCORES", theme=menus.menu_theme()
        )
        settings = menus.create_settings_menu(settings_choices)
        confirmation = menus.create_confirmation_menu(confirmation_choices)
        intro = menus.create_intro_menu(self.toggle_pause)
        pause = menus.create_pause_menu(pause_choices)
        self.menu = Menu(main_menu, high_scores, settings, confirmation, intro, pause)
        self.current_menu = self.menu.main_menu

    # Sets the current menu to the main menu
    def set_main_menu(self):
        if self.paused:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(MBGM)
            pygame.mixer.music.play(-1)
            self.paused = False
            if not self.music:
                pygame.mixer.music.pause()

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
        self.preview_color("./assets/sprites/CHARACTER_SPRITES/Red/")

    # Sets the current menu to the high score menu
    def set_high_scores_menu(self):
        self.current_menu.disable()
        self.current_menu = self.menu.high_scores
        self.current_menu.clear()

        for score in self.high_scores:
            name, value = score.strip().split(":")
            self.current_menu.add_label(f"{name:<15}{value:>15}")

        for _ in range(10 - len(self.high_scores)):
            self.current_menu.add_label("")

        self.current_menu.add_button("BACK", self.set_main_menu)
        self.current_menu.set_sound(menus.SOUND)
        self.current_menu.enable()

    # Sets the current menu to the settings menu
    def set_settings_menu(self):
        if self.back_sfx:
            menus.SOUND.play_close_menu()

        self.back_sfx = False
        self.current_menu.disable()
        self.current_menu = self.menu.settings
        self.current_menu.enable()

    # Confirmation menu for deleting high scores
    def set_confirmation_menu(self):
        self.back_sfx = True
        self.current_menu.disable()
        self.current_menu = self.menu.confirmation
        self.current_menu.enable()

    # Pause menu
    def toggle_pause(self):
        menus.SOUND.play_event()
        if self.paused:
            print("unpaused")
            pygame.mixer.music.set_volume(0.4)
            self.paused = False
            self.current_menu.disable()
            self.display.blit(BG, (0, 0))
        else:
            print("paused")
            pygame.mixer.music.set_volume(0.1)
            self.paused = True
            self.current_menu = self.menu.pause
            self.current_menu.enable()

        self.play_game()

    # Used to set the player color in the play menu
    def set_player_color(self, _, path):
        menus.SOUND.play_event()
        self.pcolor = path
        self.preview_color(path)

    def preview_color(self, path):
        frame = 0
        preview = Sprite(path + "idle.png", 5, upscale=2)
        sprites = pygame.sprite.OrderedUpdates()
        surface = self.display.copy()
        self.running_preview = True
        clock = pygame.time.Clock()
        next_frame = pygame.time.get_ticks()
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
        self.state.set_difficulty(difficulty)

    # Toggle between fs and windowed
    def toggle_fs(self, _, __):
        menus.SOUND.play_event()
        if self.fs:
            pygame.display.toggle_fullscreen()
            self.display = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
            self.fs = False
        else:
            self.display = pygame.display.set_mode(
                [WIDTH, HEIGHT], pygame.SCALED | pygame.FULLSCREEN
            )
            self.fs = True

    # Toggle music
    def toggle_music(self, _, __):
        menus.SOUND.play_event()
        if self.music:
            pygame.mixer.music.pause()
            self.music = False
        else:
            pygame.mixer.music.unpause()
            self.music = True

    # Gets the high scores from the text file and stores it in a list
    def get_high_scores(self):
        with open("high_scores.txt") as f:
            self.high_scores = f.readlines()

        self.high_scores.sort(
            key=lambda score: int(score.split(":")[1].strip()), reverse=True
        )

    # Clears the high scores
    def clear_high_scores(self):
        self.back_sfx = False
        menus.SOUND.play_error()

        with open("high_scores.txt", "w") as f:
            f.truncate(0)

        self.high_scores = []
        self.set_settings_menu()


if __name__ == "__main__":
    game = CovidBlaster()
    game.run()
