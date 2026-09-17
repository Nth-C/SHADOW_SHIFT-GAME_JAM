import pygame as pg

from entity import Entity


class Enemy(Entity):
    def __init__(self, x: int, y: int, width: int = 64, height: int = 64, hp: int = 30, attack: int = 10, speed: int = 1, aggro_range: int = 100):
        
        super().__init__(x, y, color=(255, 0, 0), width=width, height=height, hp=hp, attack=attack, speed=speed)

        self.max_hp = hp
        self.aggro_range = aggro_range
        
        self.width = width
        self.height = height


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

    def update(self, player) -> None:
        attack_range = self.get_aggro_range()

        # si le joueur entre dans la range l'enemie lui fonce dessus
        if player.rect.colliderect(attack_range):
            if self.rect.x < player.rect.x:
                self.change_animation('right')
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.change_animation('left')
                self.rect.x -= self.speed
                
            if self.rect.y < player.rect.y:
                self.change_animation('down')
                self.rect.y += self.speed
            elif self.rect.y > player.rect.y:
                self.change_animation('up')
                self.rect.y -= self.speed        

    def draw_hp_bar(self, surface: pg.Surface, offset_rect: pg.Rect) -> None:
        if self.hp > 0:
            ratio = self.hp / self.max_hp
            
            bar_width = offset_rect.width
            bar_height = 5
            
            x = offset_rect.x
            y = offset_rect.y
            
            pg.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height))
            pg.draw.rect(surface, (255, 50, 50), (x, y, bar_width * ratio, bar_height))

    # affiche la zone d'agrro
    def draw_aggro_range(self, surface: pg.Surface, offset_rect: pg.Rect) -> None:        
        calque = pg.Surface((self.aggro_range * 2, self.aggro_range * 2), pg.SRCALPHA)
       
        pg.draw.circle(calque, (240, 128, 128, 100), (self.aggro_range, self.aggro_range), self.aggro_range, 0)
        
        pos_x = offset_rect.centerx - self.aggro_range
        pos_y = offset_rect.centery - self.aggro_range
        
        surface.blit(calque, (pos_x, pos_y))

    def get_aggro_range(self) -> pg.Rect:
        taille = self.aggro_range
        zone_rect = pg.Rect(0, 0, taille, taille)
        zone_rect.center = self.rect.center
        return zone_rect