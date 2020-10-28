import pygame
import mainCharacter


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
        
        #Game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            
            
            
if __name__ == '__main__':
    print("alex was here")
    covidBlaster = StrawhatsGame()
    covidBlaster.run_game()