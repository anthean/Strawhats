import pygame_menu
from window_settings import *


# Global variables for menu properties
FONT = './assets/font/m5x7.ttf'
THEME = pygame_menu.themes.THEME_DEFAULT
THEME.title_font = FONT
THEME.widget_font = FONT
THEME.title_font_size = PX(0.04)
THEME.widget_font_size = PX(0.04)
SOUND = pygame_menu.sound.Sound()
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, './assets/sfx/menu.wav')
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_OPEN_MENU, './assets/sfx/confirm.wav')
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_CLOSE_MENU, './assets/sfx/back.wav')
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_EVENT, './assets/sfx/key.wav')
SOUND.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, './assets/sfx/delete.wav')


def create_main_menu(choice) -> pygame_menu.Menu:
    main_menu = pygame_menu.Menu(HEIGHT, WIDTH, 'COVID BLASTER', theme=THEME)
    main_menu.add_button('PLAY', choice[0])
    main_menu.add_button('HIGH SCORES', choice[1])
    main_menu.add_button('SETTINGS', choice[2])
    main_menu.add_button('QUIT', choice[3])
    main_menu.set_sound(SOUND)
    return main_menu


def create_play_menu(choice) -> pygame_menu.Menu:
    play_menu = pygame_menu.Menu(HEIGHT, WIDTH, 'COVIDBLASTER', theme=THEME)
    for _ in range(3): play_menu.add_label('')
    play_menu.add_text_input('NAME: ', default='PLAYER', maxchar=10, onchange=choice[0], onreturn=choice[0])
    play_menu.add_selector('COLOR: ',
                           [('RED', './assets/sprites/CHARACTER_SPRITES/Red/'), 
                            ('GREEN', './assets/sprites/CHARACTER_SPRITES/Green/'),
                            ('BLUE', './assets/sprites/CHARACTER_SPRITES/Blue/'),
                            ('YELLOW', './assets/sprites/CHARACTER_SPRITES/Yellow/'),
                            ('BLACK', './assets/sprites/CHARACTER_SPRITES/Black/')],
                           default=0, onchange=choice[1], onreturn=choice[1])  
    play_menu.add_selector('DIFFICULTY: ', [('NORMAL', 3), ('INSTA-DEATH', 1)], default=0, onchange=choice[2], onreturn=choice[2])
    play_menu.add_button('START', choice[3])
    play_menu.add_button('BACK', choice[4])
    play_menu.set_sound(SOUND)
    return play_menu


def create_settings_menu(choice) -> pygame_menu.Menu:
    settings_menu = pygame_menu.Menu(HEIGHT, WIDTH, 'SETTINGS', theme=THEME)
    if FULLSCREEN: settings_menu.add_selector('FULLSCREEN: ', [('ON', None), ('OFF', None)], onchange=choice[0])
    else: settings_menu.add_selector('FULLSCREEN: ', [('OFF', None), ('ON', None)], onchange=choice[0])
    settings_menu.add_selector('MUSIC: ', [('ON', None), ('OFF', None)], onchange=choice[1])
    settings_menu.add_button('CLEAR HIGH SCORES', choice[2])
    settings_menu.add_button('BACK', choice[3])
    settings_menu.set_sound(SOUND)
    return settings_menu


def create_confirmation_menu(choice) -> pygame_menu.Menu:
    confirmation_menu = pygame_menu.Menu(HEIGHT, WIDTH, 'SETTINGS', theme=THEME)
    confirmation_menu.add_label('ARE YOU SURE?')
    confirmation_menu.add_button('YES', choice[0])
    confirmation_menu.add_button('NO', choice[1])
    confirmation_menu.set_sound(SOUND)
    return confirmation_menu
