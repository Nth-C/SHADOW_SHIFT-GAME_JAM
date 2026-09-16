import pygame as pg

from enums.direction import Direction
from player.playable_entity import PlayableEntity


class Shadow(PlayableEntity):
    def __init__(self, x: int, y:int):
        super().__init__(x, y)
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
        
        self.is_defenseless = False;

        self.keypress_history: list[int] = []; # liste des touche qui sont actuellement presser
        self.current_dir_x: Direction = Direction.RIGHT; # direction dans laquel le joueur est
        self.current_dir_y: Direction = None;
        self.position = [x,y];

        self.speed = 6;

    def get_image(self, x, y):
        image = pg.Surface([32, 32], pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def change_animation(self, name):
        self.image = self.images[name]