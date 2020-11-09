# Functions for menu creation are defined here to avoid clutter in CovidBlaster
import pygame_menu


# Global variable for theme
THEME = pygame_menu.themes.THEME_BLUE


def create_main_menu(resolution: tuple, choice: tuple) -> pygame_menu.Menu:
    x, y = resolution
    main_menu = pygame_menu.Menu(y, x, 'COVID BLASTER', theme=THEME)
    main_menu.add_button('Play', choice[0])
    main_menu.add_button('High Scores', choice[1])
    main_menu.add_button('Settings', choice[2])
    main_menu.add_button('Quit', choice[3])
    return main_menu


def create_play_menu(resolution: tuple, choice: tuple) -> pygame_menu.Menu:
    x, y = resolution
    play_menu = pygame_menu.Menu(y, x, 'COVID BLASTER', theme=THEME)
    play_menu.add_button('BACK', choice[1])
    return play_menu


def create_hs_menu(resolution: tuple, choice: callable) -> pygame_menu.Menu:
    x, y = resolution
    hs_menu = pygame_menu.Menu(y, x, 'HIGH SCORES', theme=THEME)
    hs_menu.add_button('BACK', choice)
    return hs_menu


def create_settings_menu(resolution: tuple, choice: tuple) -> pygame_menu.Menu:
    x, y = resolution
    settings_menu = pygame_menu.Menu(y, x, 'SETTINGS', theme=THEME)
    settings_menu.add_button('BACK', choice[1])
    return settings_menu
