import pygame
# todo:
# don't let the character move off screen
# add health modifier

class MainCharacter:
    def __init__(self, h: int, x: int, y: int):
        self.name = "chicken"
        self.health = h
        self.x_pos = x
        self.y_pos = y

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 15, 15)

    def print_name(self):
        print(self.name)

    def moveVertically(self, distance, highestDistance, smallestDistance):
        self.y_pos = self.y_pos + distance
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 15, 15)

    def moveHorizontally(self, distance, highestDistance, smallestDistance):
        self.x_pos = self.x_pos + distance
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 15, 15)             #KIM: what is highestDistance and smallestDistance supposed to be?
