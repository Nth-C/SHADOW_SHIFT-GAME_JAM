import pygame
from screen import Screen
from map import Map

class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.map.switch_map("spawn") 

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.map.draw()
            
            self.screen.update()
            clock.tick(self.screen.framerate)