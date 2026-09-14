import pygame
from game import Game

pygame.init() #[cite: 2]

if __name__ == "__main__": #[cite: 2]
    game = Game()
    game.run()
    pygame.quit()