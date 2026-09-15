import pygame as pg
from pygame.event import Event
from entity import Entity
from enums.direction import Direction
import constants.player as player_constants

class Body(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 255, 0), width=25, height=50, hp=100, attack=20, speed=4, energy=100, health=100);
        self.is_defenseless = False;

        self.keypress_history: list[int] = []; # liste des touche qui sont actuellement presser
        self.current_dir_x: Direction = Direction.RIGHT; # direction dans laquel le joueur est
        self.current_dir_y: Direction = None;

        self.last_regen_time = pg.time.get_ticks()

        self.capacity_active = false
        self.last_capacity_time = pg.time.get_ticks()


    # gere les evenement du joueur (déplacement)
    def event_handler(self, event: Event):
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
            self.dash(player_constants.DASH_DISTANCE);

        # --- capacite ombre
        # active la capacite de se spéarer de son ombre
        if event.type == pg.K_f:
            self.toggle_capacity();


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

            # si il s'est écoulé 2sec avant la derniere regen
            if current_time - self.last_regen_time >= player_constants.ENERGY_REGEN_TIME:
                self.energy += player_constants.ENERGY_REGEN
                
                if self.energy > player_constants.ENERGY_MAX:
                    self.energy = player_constants.ENERGY_MAX
                
                self.last_regen_time = current_time
            

    # dash du perso
    def dash(self, value: int) -> None:
        if self.energy >= player_constants.DASH_ENERGY_CONSUMPTION:
            self.use_energy(player_constants.DASH_ENERGY_CONSUMPTION);

            if self.current_dir_y == Direction.UP:
                self.rect.y -= value;
            elif self.current_dir_y == Direction.DOWN:
                self.rect.y += value;

            if self.current_dir_x == Direction.LEFT:
                self.rect.x -= value;
            elif self.current_dir_x == Direction.RIGHT:
                self.rect.x += value;

    # mouvement du perso
    def move(self):
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
                    self.rect.x -= self.speed;
                    self.current_dir_x = Direction.LEFT;
                    move_x = True; # verrouille l'axe x
                elif keypressed == pg.K_d:
                    self.rect.x += self.speed;
                    self.current_dir_x = Direction.RIGHT;
                    move_x = True;
                
            # --- mouvement y
            if not move_y:
                if keypressed == pg.K_z:
                    self.rect.y -= self.speed;
                    self.current_dir_y = Direction.UP;
                    move_y = True; # verrouille l'axe y
                elif keypressed == pg.K_s:
                    self.rect.y += self.speed;
                    self.current_dir_y = Direction.DOWN;
                    move_y = True;

    # active / desactive la capacité
    def toggle_capacity(self):
        # si capacité pas active alors on l'active sinon on la desactive
        if not self.capacity_active and self.energie > 0:
            self.capacity_active = true
        else :
            self.capacity_active = false
            self.last_regen_time = pg.time.get_ticks()

    # actualise l'energie du joueurs en fonction du temps d'utilisation de l'ombre
    def update_energy(self):
        current_time = pg.time.get_ticks()

        if self.capacity_active:
            if (current_time - self.last_capacity_time) >= 100:
                self.energy -= 5
                self.last_capacity_time = current_time

                if self.energy <= 0:
                    self.energy = 0
                    self.capacity_active = false
                    self.last_regen_time = current_time
        else:
            self.regen_energy()



class Shadow(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 0, 255), width=25, height=50, hp=100, attack=5, speed=6, energy=100, health=100);
        self.is_defenseless = False;

        self.keypress_history: list[int] = []; # liste des touche qui sont actuellement presser
        self.current_dir_x: Direction = Direction.RIGHT; # direction dans laquel le joueur est
        self.current_dir_y: Direction = None;

        self.last_regen_time = pg.time.get_ticks()