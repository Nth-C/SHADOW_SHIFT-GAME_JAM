import pygame as pg
from pygame.event import Event

import constants.player as player_constants
from entity import Entity
from enums.direction import Direction

# class parent de body et shadow
class PlayableEntity(Entity):
    def __init__(self, x: int, y:int):
        super().__init__(x, y, color=(0, 255, 0), width=25, height=50, hp=100, attack=20, speed=4, energy=100, health=100);

        self.keypress_history: list[int] = []; # liste des touche qui sont actuellement presser
        self.current_dir_x: Direction = Direction.RIGHT; # direction dans laquel le joueur est
        self.current_dir_y: Direction = None;
        self.is_attacking: bool = False;

        self.last_damage_time = 0

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
    
    # comsomation de l'énergie du perso
    def use_energy(self, energyToConsume: int) -> None:
        if self.energy >= energyToConsume:
            # si l'énérgie été au max on commence le timer de recuperation
            if self.energy == player_constants.ENERGY_MAX:
                self.last_regen_time = pg.time.get_ticks()

            self.energy -= energyToConsume;

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

    # recupere de l'energie toutes le 2 sec
    def regen_energy(self) -> None:
        if self.energy < player_constants.ENERGY_MAX: 
            
            current_time = pg.time.get_ticks()

            # si il s'est écoulé 2 sec avant la derniere regen
            if current_time - self.last_regen_time >= player_constants.ENERGY_REGEN_TIME:
                self.energy += player_constants.ENERGY_REGEN
                
                self.energy = min(self.energy, player_constants.ENERGY_MAX)
                
                self.last_regen_time = current_time

    def reset_movement(self):
        self.keypress_history.clear()

    # mouvement du perso
    def _move_axis(
        self,
        movement_x: int,
        movement_y: int,
        walls: list[pg.Rect] | None,
    ) -> bool:
        next_rect = self.rect.move(movement_x, movement_y)
        next_feet = self.feet.copy()
        next_feet.midbottom = next_rect.midbottom

        if walls and any(next_feet.colliderect(wall) for wall in walls):
            return False

        self.rect = next_rect
        self.feet = next_feet
        return True

    def move(self, walls: list[pg.Rect] | None = None):
        # permet de pouvoir bouger que dans une seule direction par axe
        move_x = False
        move_y = False

        if len(self.keypress_history) > 0:
            self.current_dir_x = None
            self.current_dir_y = None

        dir_x = None
        dir_y = None

        # 1ère passe : on détermine juste les directions, sans bouger encore
        for keypressed in reversed(self.keypress_history):
            if not move_x:
                if keypressed == pg.K_q:
                    dir_x = Direction.LEFT
                    move_x = True
                elif keypressed == pg.K_d:
                    dir_x = Direction.RIGHT
                    move_x = True

            if not move_y:
                if keypressed == pg.K_z:
                    dir_y = Direction.UP
                    move_y = True
                elif keypressed == pg.K_s:
                    dir_y = Direction.DOWN
                    move_y = True

        # si on bouge sur les deux axes en meme temps, on reduit la vitesse
        speed = self.speed
        if dir_x is not None and dir_y is not None:
            speed *= 0.7071  # 1 / racine(2)

        # 2eme passe : on applique le mouvement avec la vitesse corrigée
        if dir_x == Direction.LEFT:
            self._move_axis(-round(speed), 0, walls)
            self.current_dir_x = Direction.LEFT
            self.change_animation('left')
        elif dir_x == Direction.RIGHT:
            self._move_axis(round(speed), 0, walls)
            self.current_dir_x = Direction.RIGHT
            self.change_animation('right')

        if dir_y == Direction.UP:
            self._move_axis(0, -round(speed), walls)
            self.current_dir_y = Direction.UP
            self.change_animation('up')
        elif dir_y == Direction.DOWN:
            self._move_axis(0, round(speed), walls)
            self.current_dir_y = Direction.DOWN
            self.change_animation('down')