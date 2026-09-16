# enemy.py
import pygame as pg

from entity import Entity


class Enemy(Entity):
    def __init__(self, x:int, y:int, range:int = 50):
        super().__init__(x, y, color=(255, 0, 0), width=25, height=40, hp=30, attack=10, speed=1);

        original_sheet = pg.image.load('assets/characters/sprite_shadow.png').convert_alpha()
        self.sprite_sheet = pg.transform.scale(original_sheet, (96, 128))

        self.images = {
            'down': pg.transform.scale(self.get_image(0, 0), (64, 64)),
            'left': pg.transform.scale(self.get_image(0, 32), (64, 64)),
            'right': pg.transform.scale(self.get_image(64, 32), (64, 64)),
            'up': pg.transform.scale(self.get_image(0, 96), (64, 64))
        }

        small_image = self.get_image(64, 0)
        self.image = pg.transform.scale(small_image, (64, 64))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.feet = pg.Rect(0, 0, self.rect.width // 2, 12)
        self.feet.midbottom = self.rect.midbottom

        self.max_hp = 30
        self.aggro_range = range

    def get_image(self, x, y):
        image = pg.Surface([32, 32], pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def change_animation(self, name):
        self.image = self.images[name]

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
