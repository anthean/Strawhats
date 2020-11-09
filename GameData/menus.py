import pygame_menu

THEME = pygame_menu.themes.THEME_BLUE


def create_main_menu(RESOLUTION: tuple, choices: tuple) -> pygame_menu.Menu:
    x, y = RESOLUTION
    main_menu = pygame_menu.Menu(y, x, 'Covid Blaster', theme=THEME)
    main_menu.add_button('Play', choices[0])
    main_menu.add_button('High Scores', choices[1])
    main_menu.add_button('Quit', choices[2])
    return main_menu
