import pygame as pg
from player import Body
from energy_bar import EnergyBar

class HudManager:
    def __init__(self):
        # On place la barre d'énergie en haut à gauche
        self.energy_bar = EnergyBar(10, 10)
        

    # Cette méthode va lire les infos du joueur pour mettre à jour l'interface
    def draw(self, screen: pg.Surface, player: Body) -> None:
        self.energy_bar.draw(screen, player.energy)
