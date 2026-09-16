# enemy.py
import pygame as pg
from entity import Entity

class Enemy(Entity):
    def __init__(self, x:int, y:int, range:int = 50):
        super().__init__(x, y, color=(255, 0, 0), width=25, height=40, hp=30, attack=10, speed=1);

        self.max_hp = 30
        self.aggro_range = range

    # boucle de l'enemie
    def update(self, player) -> None:
        attack_range = self.get_aggro_range()

        # si le joueur entre dans la range l'enemie lui fonce dessus
        if player.rect.colliderect(attack_range):
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed
                
            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > player.rect.y:
                self.rect.y -= self.speed        

    # affiche la bar d'hp de l'enemie
    def draw_hp_bar(self, surface: pg.Surface) -> None:
        if self.hp > 0:
            ratio = self.hp / self.max_hp
            
            bar_width = self.rect.width
            bar_height = 5
            x = self.rect.x
            y = self.rect.y - 10
            
            pg.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height))
            pg.draw.rect(surface, (255, 255, 0), (x, y, bar_width * ratio, bar_height))

    # TODO a suppr c'est pour voir la range d'aggro
    def draw_aggro_range(self, surface: pg.Surface) -> None:
        taille = self.aggro_range * 5
        zone_rect = pg.Rect(0, 0, taille, taille)
        zone_rect.center = self.rect.center
        
        pg.draw.rect(surface, (255, 255, 0), zone_rect, 1)

    # recupere la zone d'aggro autour de l'enemie
    def get_aggro_range(self) -> pg.Rect:
        taille = self.aggro_range * 5;
        zone_rect = pg.Rect(0, 0, taille, taille);
        zone_rect.center = self.rect.center;

        return zone_rect
