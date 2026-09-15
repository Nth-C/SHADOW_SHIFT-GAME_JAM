import pygame as pg
from player import Body
from .energy_bar import EnergyBar

class HudManager:
    def __init__(self):
        # on place la barre d'énergie / heal en haut à gauche
        self.energy_bar = EnergyBar(10, 10)
        #self.health_bar = EnergyBar(50, 10)

    # lire les infos du joueur pour mettre à jour l'hud
    def draw(self, screen: pg.Surface, player: Body) -> None:
        self.energy_bar.draw(screen, player.energy);
        #self.health_bar.draw(screen, player.energy);

