import pygame

class Screen: 

    def __init__(self):
        self.display = pygame.display.set_mode((1024, 768))
        self.framerate = 60

    def update(self):
        pygame.display.flip()
        pygame.display.update()
        self.display.fill((0,0,0))

    def get_size(self):
        return self.display.get_size()

    def get_display(self):
        return self.display