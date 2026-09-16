import pygame as pg
from pygame.event import Event

import constants.player as player_constants
from entity import Entity
from enums.direction import Direction
from player.playable_entity import PlayableEntity

class Body(PlayableEntity):
    def __init__(self, x: int, y:int):
        super().__init__(x, y)

        original_sheet = pg.image.load('assets/characters/sprite_perso.png').convert_alpha()
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

        self.position = [x,y];

        self.old_position = self.position.copy()
        self.last_regen_time = pg.time.get_ticks()
        self.capacity_active = False
        self.last_capacity_time = pg.time.get_ticks()

    def get_image(self, x, y):
        image = pg.Surface([32, 32], pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def change_animation(self, name):
        self.image = self.images[name]

    def save_location(self): self.old_position = self.position.copy()

    def moove_back(self):
        self.position = self.old_position

    def event_handler(self, event: Event, walls: list[pg.Rect] | None = None):
        super().event_handler(event, walls)

        # --- dash
        # dash dans la derniere direction
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.dash(player_constants.DASH_DISTANCE, walls);

    
    # dash du perso
    def dash(self, value: int, walls: list[pg.Rect] | None = None) -> None:
        if self.energy >= player_constants.DASH_ENERGY_CONSUMPTION:
            self.use_energy(player_constants.DASH_ENERGY_CONSUMPTION);

            if self.current_dir_y == Direction.UP:
                self._move_axis(0, -value, walls)
            elif self.current_dir_y == Direction.DOWN:
                self._move_axis(0, value, walls)

            if self.current_dir_x == Direction.LEFT:
                self._move_axis(-value, 0, walls)
            elif self.current_dir_x == Direction.RIGHT:
                self._move_axis(value, 0, walls)



    # permet de gerer l'invincibilité apres un degat
    def take_damage(self, amount: int) -> None:
        current_time = pg.time.get_ticks()

        if current_time - self.last_damage_time >= player_constants.INVINCIBLILITY_DURATION:

            # met les degat
            super().take_damage(amount)
            
            self.last_damage_time = current_time
    
    # active / desactive la capacité
    def toggle_capacity(self):
        # si capacité pas active alors on l'active sinon on la desactive
        if not self.capacity_active and self.energy > 0:
            self.capacity_active = True
            self.speed = 0
        else :
            self.capacity_active = False
            self.last_regen_time = pg.time.get_ticks()
            self.speed = 4

    # actualise l'energie du joueurs en fonction du temps d'utilisation de l'ombre
    def update_energy(self):
        current_time = pg.time.get_ticks()

        if self.capacity_active:
            if (current_time - self.last_capacity_time) >= 200:
                self.energy -= 5
                self.last_capacity_time = current_time

                if self.energy <= 0:
                    self.energy = 0
                    self.capacity_active = False
                    self.last_regen_time = current_time
                    self.speed = 4
        else:
            self.regen_energy()
