import pygame as pg


class EnergyBar:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 20
        self.max_energy = 100

    def draw(self, screen: pg.Surface, current_energy: int) -> None:
        ratio = current_energy / self.max_energy
        
        # fond
        pg.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        # barre
        pg.draw.rect(screen, (0, 100, 255), (self.x, self.y, self.width * ratio, self.height))