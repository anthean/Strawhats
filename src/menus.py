from copy import deepcopy

import pygame_menu

from window_settings import *

SOUND = pygame_menu.sound.Sound()
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, "./assets/sfx/menu.wav")
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_OPEN_MENU, "./assets/sfx/confirm.wav")
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_CLOSE_MENU, "./assets/sfx/back.wav")
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_EVENT, "./assets/sfx/key.wav")
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, "./assets/sfx/delete.wav")


def menu_theme():
    menu_theme = deepcopy(pygame_menu.themes.THEME_DEFAULT)
    menu_theme.title_font = "./assets/font/m5x7.ttf"
    menu_theme.widget_font = "./assets/font/m5x7.ttf"
    menu_theme.title_font_size = PX(0.04)
    menu_theme.widget_font_size = PX(0.04)
    return menu_theme


def game_theme():
    game_theme = deepcopy(pygame_menu.themes.THEME_DARK)
    game_theme.title_font = "./assets/font/m5x7.ttf"
    game_theme.widget_font = "./assets/font/m5x7.ttf"
    game_theme.title_font_size = PX(0.04)
    game_theme.widget_font_size = PX(0.04)
    img = pygame_menu.baseimage.BaseImage(
        "./assets/sprites/STAGE/dark.png", pygame_menu.baseimage.IMAGE_MODE_FILL, (0, 0)
    )
    game_theme.background_color = img
    return game_theme


def create_main_menu(choice):
    main_menu = pygame_menu.Menu(HEIGHT, WIDTH, "COVID BLASTER", theme=menu_theme())
    main_menu.add_button("PLAY", choice[0])
    main_menu.add_button("HIGH SCORES", choice[1])
    main_menu.add_button("SETTINGS", choice[2])
    main_menu.add_button("QUIT", choice[3])
    main_menu.set_sound(SOUND)
    return main_menu


def create_play_menu(choice):
    play_menu = pygame_menu.Menu(HEIGHT, WIDTH, "COVIDBLASTER", theme=menu_theme())
    for _ in range(3):
        play_menu.add_label("")
    play_menu.add_text_input(
        "NAME: ",
        default=getpass.getuser().upper(),
        maxchar=10,
        onchange=choice[0],
        onreturn=choice[0],
    )

    play_menu.add_selector(
        "COLOR: ",
        [
            ("RED", "./assets/sprites/CHARACTER_SPRITES/Red/"),
            ("GREEN", "./assets/sprites/CHARACTER_SPRITES/Green/"),
            ("BLUE", "./assets/sprites/CHARACTER_SPRITES/Blue/"),
            ("YELLOW", "./assets/sprites/CHARACTER_SPRITES/Yellow/"),
            ("BLACK", "./assets/sprites/CHARACTER_SPRITES/Black/"),
        ],
        default=0,
        onchange=choice[1],
        onreturn=choice[1],
    )

    play_menu.add_selector(
        "DIFFICULTY: ",
        [("NORMAL", 3), ("INSTA-DEATH", 1)],
        default=0,
        onchange=choice[2],
        onreturn=choice[2],
    )
    play_menu.add_button("START", choice[3])
    play_menu.add_button("BACK", choice[4])
    play_menu.set_sound(SOUND)
    return play_menu


def create_settings_menu(choice):
    settings_menu = pygame_menu.Menu(HEIGHT, WIDTH, "SETTINGS", theme=menu_theme())
    if FULLSCREEN:
        settings_menu.add_selector(
            "FULLSCREEN: ", [("ON", None), ("OFF", None)], onchange=choice[0]
        )
    else:
        settings_menu.add_selector(
            "FULLSCREEN: ", [("OFF", None), ("ON", None)], onchange=choice[0]
        )
    settings_menu.add_selector(
        "MUSIC: ", [("ON", None), ("OFF", None)], onchange=choice[1]
    )
    settings_menu.add_button("CLEAR HIGH SCORES", choice[2])
    settings_menu.add_button("BACK", choice[3])
    settings_menu.set_sound(SOUND)
    return settings_menu


def create_confirmation_menu(choice):
    confirmation_menu = pygame_menu.Menu(HEIGHT, WIDTH, "SETTINGS", theme=menu_theme())
    confirmation_menu.add_label("ARE YOU SURE?")
    confirmation_menu.add_button("YES", choice[0])
    confirmation_menu.add_button("NO", choice[1])
    confirmation_menu.set_sound(SOUND)
    return confirmation_menu


def create_intro_menu(choice):
    intro_menu = pygame_menu.Menu(HEIGHT, WIDTH, "COVIDBLASTER", theme=game_theme())
    intro_menu.add_label("DERANGED CITIZENS INFECTED WITH COVID-19 HAVE GONE MAD AND")
    intro_menu.add_label("ARE NOT PRACTICING SAFE SOCIAL DISTANCING MEASURES.")
    intro_menu.add_label("TAKE THEM OUT AND SURVIVE AS LONG AS YOU CAN.")
    intro_menu.add_label("")
    intro_menu.add_button("CONTINUE", choice)
    intro_menu.set_sound(SOUND)
    return intro_menu


def create_pause_menu(choice):
    pause_menu = pygame_menu.Menu(HEIGHT, WIDTH, "COVIDBLASTER", theme=game_theme())
    pause_menu.add_label("PAUSED")
    for _ in range(2):
        pause_menu.add_label("")
    pause_menu.add_button("CONTINUE", choice[0])
    pause_menu.add_button("QUIT", choice[1])
    pause_menu.set_sound(SOUND)
    return pause_menu
