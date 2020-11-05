import pygame, sys
import mainCharacter

# Game stats
_FRAME_RATE = 10
_FRAME_WIDTH = 800
_FRAME_HEIGHT = 600
_BACKGROUND_COLOR = pygame.Color(100, 100, 100)

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 225)
teal = pygame.Color(0, 255, 255)
yellow = pygame.Color(255, 255, 0)
pink = pygame.Color(255, 0, 255)
black = pygame.Color(0, 0, 0)
colors = [red, green, blue, teal, yellow, pink]


# Character stats
_charHealth = 100
_charXPos = 400
_charYPos = 300
charSpeed = 10



# test
class StrawhatsGame:
    def __init__(self):
        self.running = True
        self.pixelWidth = _FRAME_WIDTH
        self.pixelHeight = _FRAME_HEIGHT
        # self.surface will be made when create_surface is called
        self.charMovingLeft = False # if left key is held down, this will be true. Some reason, can't make this a global variable
        self.charMovingRight = False
        self.charMovingUp = False
        self.charMovingDown = False
        self.charShooting = False

    def run_game(self):
        # Initializes and runs CovidBlaster through Pygame
        # Pygame initialization
        pygame.init()

        try:
            clock = pygame.time.Clock()
            self.surface = pygame.display.set_mode((self.pixelWidth, self.pixelHeight))

            test_surface = pygame.Surface((100, 200))
            test_surface.fill((0, 0, 100))

            # create game character
            character = mainCharacter.MainCharacter(_charHealth, _charXPos, _charYPos)

            while self.running:
                clock.tick(_FRAME_RATE)

                # handle events
                self.handle_events(character)

                # draw frames
                self.draw_frames()

                self.surface.blit(test_surface, (100, 100))
                self.surface.blit(character.image, character.rect)
                pygame.display.update()

        finally:
            pygame.quit()
            sys.exit()

    def handle_events(self, character) -> None:
        """ loops through events from pygame """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            """ MOVED HANDLING BUTTON PRESSES UP HERE """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.charMovingLeft = True
                if event.key == pygame.K_RIGHT:
                    self.charMovingRight = True
                if event.key == pygame.K_UP:
                    self.charMovingUp = True
                if event.key == pygame.K_DOWN:
                    self.charMovingDown = True
                if event.key == pygame.K_SPACE:
                    self.charShooting = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.charMovingLeft = False
                if event.key == pygame.K_RIGHT:
                    self.charMovingRight = False
                if event.key == pygame.K_UP:
                    self.charMovingUp = False
                if event.key == pygame.K_DOWN:
                    self.charMovingDown = False
                if event.key == pygame.K_SPACE:
                    self.charShooting = False

        # outside of for loop, called once every game iteration
        if self.charMovingLeft:
            character.moveHorizontally(-charSpeed)
        if self.charMovingRight:
            character.moveHorizontally(charSpeed)
        if self.charMovingUp:
            character.moveVertically(-charSpeed)
        if self.charMovingDown:
            character.moveVertically(charSpeed)
        if self.charShooting:
            print("shoot")

    def draw_frames(self):
        """ called in main method. responsible for refreshing frame after each call """
        self.surface.fill(_BACKGROUND_COLOR)
        pygame.display.update()


if __name__ == '__main__':
    covidBlaster = StrawhatsGame()
    covidBlaster.run_game()
