import pygame
import pygame_menu
import menus

# Global variables for window settings
WIDTH = 800
HEIGHT = 600
RESOLUTION = (WIDTH, HEIGHT)
FPS = 60


class CovidBlaster:
    def __init__(self):
        self.display = None
        self.current_menu = None

    def run(self):
        pygame.init()
        self.initialize_window()
        self.current_menu = menus.create_main_menu(RESOLUTION, (self.play, self.high_scores, pygame_menu.events.EXIT))
        self.current_menu.mainloop(self.display)

    def initialize_window(self):
        self.display = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)

    def play(self):
        return None

    def high_scores(self):
        return None


if __name__ == '__main__':
    game = CovidBlaster()
    game.run()