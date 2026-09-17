import pygame as pg

from player.body import Body

from .energy_bar import EnergyBar
from .health_bar import HealthBar


class HudManager:
    def __init__(self):
        # on place la barre d'énergie / heal en haut à gauche
        self.health_bar = HealthBar(10, 10)
        self.energy_bar = EnergyBar(10, 40)

    # lire les infos du joueur pour mettre à jour l'hud
    def draw(self, screen: pg.Surface, player: Body) -> None:
        self.energy_bar.draw(screen, player.energy)
        self.health_bar.draw(screen, player.hp)
