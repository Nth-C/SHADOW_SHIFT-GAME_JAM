import pygame as pg
from pygame.event import Event

import constants.player as player_constants
from entity import Entity
from enums.direction import Direction


class Body(Entity):
    def __init__(self, x: int, y:int):
        super().__init__(x, y, color=(0, 255, 0), width=25, height=50, hp=100, attack=20, speed=4, energy=100, health=100);
        
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
        
        self.is_defenseless = False;

        self.keypress_history: list[int] = []; # liste des touche qui sont actuellement presser
        self.current_dir_x: Direction = Direction.RIGHT; # direction dans laquel le joueur est
        self.current_dir_y: Direction = None;
        self.is_attacking: bool = False;

        self.last_damage_time = 0
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

    # gere les evenement du joueur (déplacement)
    def event_handler(self, event: Event, walls: list[pg.Rect] | None = None):
        # liste avec les boutons de directions
        key_move = [pg.K_q, pg.K_d, pg.K_z, pg.K_s];

        # --- mouvement 
        # si on appuie sur un bouton et que c'est un bouton de mouvement
        if event.type == pg.KEYDOWN and event.key in key_move:
            # si on réappuie sur le meme bouton on le remet à la fin
            if event.key in self.keypress_history:
                self.keypress_history.remove(event.key);
            self.keypress_history.append(event.key);

        # ou si on relache un bouton qui est un bouton de mouvement
        elif event.type == pg.KEYUP and event.key in key_move:
            if event.key in self.keypress_history:
                self.keypress_history.remove(event.key);

        # --- dash
        # dash dans la derniere direction
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.dash(player_constants.DASH_DISTANCE, walls);

        

        # --- attaque
        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            self.is_attacking = True;

    # comsomation de l'énergie du perso
    def use_energy(self, energyToConsume: int) -> None:
        if self.energy >= energyToConsume:
            # si l'énérgie été au max on commence le timer de recuperation
            if self.energy == player_constants.ENERGY_MAX:
                self.last_regen_time = pg.time.get_ticks()

            self.energy -= energyToConsume;


    # recupere de l'energie toutes le 2 sec
    def regen_energy(self) -> None:
        if self.energy < player_constants.ENERGY_MAX: 
            
            current_time = pg.time.get_ticks()

            # si il s'est écoulé 2 sec avant la derniere regen
            if current_time - self.last_regen_time >= player_constants.ENERGY_REGEN_TIME:
                self.energy += player_constants.ENERGY_REGEN
                
                self.energy = min(self.energy, player_constants.ENERGY_MAX)
                
                self.last_regen_time = current_time
            

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

    # mouvement du perso
    def _move_axis(
        self,
        movement_x: int,
        movement_y: int,
        walls: list[pg.Rect] | None,
    ) -> None:
        next_rect = self.rect.move(movement_x, movement_y)
        next_feet = self.feet.copy()
        next_feet.midbottom = next_rect.midbottom

        if not walls or not any(next_feet.colliderect(wall) for wall in walls):
            self.rect = next_rect
            self.feet = next_feet

    def move(self, walls: list[pg.Rect] | None = None):
        # permet de pouvoir bouger que dans une seule direction
        move_x = False;
        move_y = False;

        # si le joueur bouge on reinisialie tout (pour le dash si on est arreter)
        if len(self.keypress_history) > 0:
            self.current_dir_x = None;
            self.current_dir_y = None;
            
        # parcours les touches presser a l'envers pour pouvoir donner la priorité a la touche la plus récente
        for keypressed in reversed(self.keypress_history):
                
            # --- mouvement x
            if not move_x:
                if keypressed == pg.K_q:
                    self._move_axis(-self.speed, 0, walls)
                    self.current_dir_x = Direction.LEFT;
                    self.change_animation('left')
                    move_x = True; # verrouille l'axe x
                elif keypressed == pg.K_d:
                    self._move_axis(self.speed, 0, walls)
                    self.current_dir_x = Direction.RIGHT;
                    self.change_animation('right')
                    move_x = True;
                
            # --- mouvement y
            if not move_y:
                if keypressed == pg.K_z:
                    self._move_axis(0, -self.speed, walls)
                    self.current_dir_y = Direction.UP;
                    self.change_animation('up')
                    move_y = True; # verrouille l'axe y
                elif keypressed == pg.K_s:
                    self._move_axis(0, self.speed, walls)
                    self.current_dir_y = Direction.DOWN;
                    self.change_animation('down')
                    move_y = True;

    # permet de gerer l'invincibilité apres un degat
    def take_damage(self, amount: int) -> None:
        current_time = pg.time.get_ticks()

        if current_time - self.last_damage_time >= player_constants.INVINCIBLILITY_DURATION:

            # met les degat
            super().take_damage(amount)
            
            self.last_damage_time = current_time

    # recupere la position de l'attaque
    def get_attack_range(self) -> pg.Rect:
        attack_rect = pg.Rect(0, 0, 40, 40)
        attack_rect.center = self.rect.center 
        
        if self.current_dir_x == Direction.LEFT:
            attack_rect.centerx -= 30
        elif self.current_dir_x == Direction.RIGHT:
            attack_rect.centerx += 30
            
        if self.current_dir_y == Direction.UP:
            attack_rect.centery -= 30
        elif self.current_dir_y == Direction.DOWN:
            attack_rect.centery += 30
            
        return attack_rect
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



class Shadow(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 0, 255), width=25, height=50, hp=100, attack=20, speed=6, energy=100, health=100);
        
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

        self.is_attacking: bool = False;

    def get_image(self, x, y):
        image = pg.Surface([32, 32], pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def change_animation(self, name):
        self.image = self.images[name]

    # gere les evenement du joueur (déplacement)
    def event_handler(self, event: Event, walls: list[pg.Rect] | None = None):
        # liste avec les boutons de directions
        key_move = [pg.K_q, pg.K_d, pg.K_z, pg.K_s];

        # --- mouvement 
        # si on appuie sur un bouton et que c'est un bouton de mouvement
        if event.type == pg.KEYDOWN and event.key in key_move:
            # si on réappuie sur le meme bouton on le remet à la fin
            if event.key in self.keypress_history:
                self.keypress_history.remove(event.key);
            self.keypress_history.append(event.key);

        # ou si on relache un bouton qui est un bouton de mouvement
        elif event.type == pg.KEYUP and event.key in key_move:
            if event.key in self.keypress_history:
                self.keypress_history.remove(event.key);

        # --- attaque
        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            self.is_attacking = True;

    # mouvement du perso
    def _move_axis(
        self,
        movement_x: int,
        movement_y: int,
        walls: list[pg.Rect] | None,
    ) -> None:
        next_rect = self.rect.move(movement_x, movement_y)
        next_feet = self.feet.copy()
        next_feet.midbottom = next_rect.midbottom

        if not walls or not any(next_feet.colliderect(wall) for wall in walls):
            self.rect = next_rect
            self.feet = next_feet

    # TODO factoriser les 2 move
    def move(self, walls: list[pg.Rect] | None = None):
        # permet de pouvoir bouger que dans une seule direction
        move_x = False;
        move_y = False;

        # si le joueur bouge on reinisialie tout (pour le dash si on est arreter)
        if len(self.keypress_history) > 0:
            self.current_dir_x = None;
            self.current_dir_y = None;
            
        # parcours les touches presser a l'envers pour pouvoir donner la priorité a la touche la plus récente
        for keypressed in reversed(self.keypress_history):
                
            # --- mouvement x
            if not move_x:
                if keypressed == pg.K_q:
                    self._move_axis(-self.speed, 0, walls)
                    self.current_dir_x = Direction.LEFT;
                    self.change_animation('left')
                    move_x = True; # verrouille l'axe x
                elif keypressed == pg.K_d:
                    self._move_axis(self.speed, 0, walls)
                    self.current_dir_x = Direction.RIGHT;
                    self.change_animation('right')
                    move_x = True;
                
            # --- mouvement y
            if not move_y:
                if keypressed == pg.K_z:
                    self._move_axis(0, -self.speed, walls)
                    self.current_dir_y = Direction.UP;
                    self.change_animation('up')
                    move_y = True; # verrouille l'axe y
                elif keypressed == pg.K_s:
                    self._move_axis(0, self.speed, walls)
                    self.current_dir_y = Direction.DOWN;
                    self.change_animation('down')
                    move_y = True;

    # recupere la position de l'attaque
    def get_attack_range(self) -> pg.Rect:
        attack_rect = pg.Rect(0, 0, 40, 40)
        attack_rect.center = self.rect.center 
        
        if self.current_dir_x == Direction.LEFT:
            attack_rect.centerx -= 30
        elif self.current_dir_x == Direction.RIGHT:
            attack_rect.centerx += 30
            
        if self.current_dir_y == Direction.UP:
            attack_rect.centery -= 30
        elif self.current_dir_y == Direction.DOWN:
            attack_rect.centery += 30
            
        return attack_rect
