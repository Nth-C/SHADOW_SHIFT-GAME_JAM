import pygame as pg


class HealthBar:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 300
        self.height = 20
        self.maxhealth = 100

    def draw(self, screen: pg.Surface, current_health: int) -> None:
        ratio = current_health / self.maxhealth
        
        # fond
        pg.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        # barre
        pg.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width * ratio, self.height))