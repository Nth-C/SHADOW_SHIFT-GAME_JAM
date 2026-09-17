import pygame as pg

from entity import Entity
from enums.direction import Direction


class EnemiesEntity(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        hp: int,
        attack: int,
        speed: int,
        aggro_range: int,
    ):
        super().__init__(
            x, y, width=width, height=height, hp=hp, attack=attack, speed=speed
        )

        self.max_hp = hp
        self.aggro_range = aggro_range
        self.width = width
        self.height = height

        self.images = {}
        self.current_direction = Direction.DOWN

    def change_animation(self, direction: Direction):
        if self.current_direction != direction and direction in self.images:
            self.current_direction = direction
            self.image = self.images[direction]

    def move_axis(
        self, movement_x: int, movement_y: int, walls: list[pg.Rect] | None
    ) -> bool:
        next_rect = self.rect.move(movement_x, movement_y)
        next_feet = self.feet.copy()
        next_feet.midbottom = next_rect.midbottom

        if walls and any(next_feet.colliderect(wall) for wall in walls):
            return False

        self.rect = next_rect
        self.feet = next_feet
        return True

    def update(self, player, walls: list[pg.Rect] | None = None) -> None:
        attack_range = self.get_aggro_range()

        if player.rect.colliderect(attack_range):
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Déplacement X
            if self.rect.x < player.rect.x:
                self.move_axis(self.speed, 0, walls)
            elif self.rect.x > player.rect.x:
                self.move_axis(-self.speed, 0, walls)

            # Déplacement Y
            if self.rect.y < player.rect.y:
                self.move_axis(0, self.speed, walls)
            elif self.rect.y > player.rect.y:
                self.move_axis(0, -self.speed, walls)

            # Animation
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.change_animation(Direction.RIGHT)
                else:
                    self.change_animation(Direction.LEFT)
            else:
                if dy > 0:
                    self.change_animation(Direction.DOWN)
                elif dy < 0:
                    self.change_animation(Direction.UP)

    def draw_hp_bar(self, surface: pg.Surface, offset_rect: pg.Rect) -> None:
        if self.hp > 0:
            ratio = self.hp / self.max_hp
            bar_width = offset_rect.width
            bar_height = 5
            x = offset_rect.x
            y = offset_rect.y

            pg.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height))
            pg.draw.rect(surface, (255, 50, 50), (x, y, bar_width * ratio, bar_height))

    def draw_aggro_range(self, surface: pg.Surface, offset_rect: pg.Rect) -> None:
        calque = pg.Surface((self.aggro_range * 2, self.aggro_range * 2), pg.SRCALPHA)
        pg.draw.circle(
            calque,
            (240, 128, 128, 100),
            (self.aggro_range, self.aggro_range),
            self.aggro_range,
            0,
        )
        pos_x = offset_rect.centerx - self.aggro_range
        pos_y = offset_rect.centery - self.aggro_range
        surface.blit(calque, (pos_x, pos_y))

    def get_aggro_range(self) -> pg.Rect:
        taille = self.aggro_range
        zone_rect = pg.Rect(0, 0, taille, taille)
        zone_rect.center = self.rect.center
        return zone_rect

    def is_dead(self) -> bool:
        return self.hp <= 0
