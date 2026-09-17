import pygame as pg
from enemies.enemies_entity import EnemiesEntity
from enums.direction import Direction


class Boss(EnemiesEntity):
    def __init__(self, x: int, y: int, width: int = 128, height: int = 128, hp: int = 200, attack: int = 20, speed: int = 1, aggro_range: int = 300):
        super().__init__(x, y, width=width, height=height, hp=hp, attack=attack, speed=speed, aggro_range=aggro_range)

        original_sheet = pg.image.load('assets/characters/boss_robot_walk.png').convert_alpha()
        self.sprite_sheet = original_sheet

        cw = 506
        ch = 506

        self.images = {
            Direction.DOWN: self.get_image(0, 0, cw, ch),
            Direction.LEFT: self.get_image(518, 0, cw, ch),
            Direction.RIGHT: self.get_image(0, 518, cw, ch),
            Direction.UP: self.get_image(518, 5138, cw, ch),
        }

        self.image = self.images[self.current_direction]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Adjust the feet rect for collision (plus grand pour le boss)
        self.feet = pg.Rect(0, 0, self.rect.width // 2, 24)
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, src_x, src_y, cell_w, cell_h):
        # Crée une surface transparente de la taille de la case brute
        image = pg.Surface([cell_w, cell_h], pg.SRCALPHA)
        # Découpe la bonne partie de la grille
        image.blit(self.sprite_sheet, (0, 0), (src_x, src_y, cell_w, cell_h))
        # Redimensionne directement à la taille finale d'affichage (128x128)
        return pg.transform.scale(image, (self.width, self.height))