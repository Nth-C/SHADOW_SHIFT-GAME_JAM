import pygame as pg

from enemies.enemies_entity import EnemiesEntity

class Enemy(EnemiesEntity):
    def __init__(self, x: int, y: int, width: int = 64, height: int = 64, hp: int = 30, attack: int = 10, speed: int = 1, aggro_range: int = 100):
        
        super().__init__(x, y, width=width, height=height, hp=hp, attack=attack, speed=speed, aggro_range=aggro_range)

        original_sheet = pg.image.load('assets/characters/sprite_robot.png').convert_alpha()
        self.sprite_sheet = pg.transform.scale(original_sheet, (96, 128))

        self.images = {
            'down': pg.transform.scale(self.get_image(32, 0), (self.width, self.height)),
            'left': pg.transform.scale(self.get_image(64, 32), (self.width, self.height)),
            'right': pg.transform.scale(self.get_image(0, 32), (self.width, self.height)),
            'up': pg.transform.scale(self.get_image(32, 96), (self.width, self.height))
        }

        small_image = self.get_image(64, 0)
        self.image = pg.transform.scale(small_image, (self.width, self.height))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.feet = pg.Rect(0, 0, self.rect.width // 2, 12)
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pg.Surface([32, 32], pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def change_animation(self, name):
        self.image = self.images[name]

