# TODO:
# add clock
# add character to screen
# add surface to draw on

#testting


import pygame
import mainCharacter

_charHealth = 100
_charXPos = 400
_charYPos = 300

#test
class StrawhatsGame:
    def __init__(self):
        self.running = False
        
    def run_game(self):
    #Initializes and runs CovidBlaster through Pygame
        #Screen initialization
        pygame.init()
        screen = pygame.display.set_mode( (800, 600) )
        
        running = True

        # create game character
        character = mainCharacter.MainCharacter(_charHealth, _charXPos, _charYPos)
        character.print_name() #prints chicken to the console

        #Game loop
        while running:

            #draw character model here


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # if arrow key is hit
                    # move character up
                    
            
            
            
if __name__ == '__main__':
    covidBlaster = StrawhatsGame()
    covidBlaster.run_game()