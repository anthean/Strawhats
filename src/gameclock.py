# from window_settings import *

# clockfont = pygame.font.Font("./assets/font/m5x7.ttf", PX(0.04))

# class GameClock(pygame.sprite.Sprite):
#     def __init__(self):
#         self.sprite.Sprite.__init__(self)
#         self.sec_int = 0
#         self.min_int = 0

#         self.sec = clockfont.render(str(self.sec_int).zfill(2), True, (255,255,255))        
#         self.min = clockfont.render(str(self.min_int).zfill(2)+' :', True, (255,255,255))

#         self.lastframe = 0


#     def update(self, display, surface):
#         surface.blit(BG, (0, 0))

#         self.sec = clockfont.render(str(self.sec_int).zfill(2), True, (255,255,255))
#         self.min = clockfont.render(str(self.min_int).zfill(2)+' :', True, (255,255,255))


#         self.sec_int += 1

#         display.blit(self.sec, (PX(0.53), PY(0.05)))
#         display.blit(self.min, (PX(0.48), PY(0.05)))


#         if self.sec_int == 60:
#             self.sec_int = 0
#             self.min_int += 1

#         if self.min_int == 60:
#             self.sec_int = 0
#             self.min_int = 0
