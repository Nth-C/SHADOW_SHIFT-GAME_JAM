import pygame as pg
from pygame.event import Event
from pygame.key import ScancodeWrapper
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
        self.position = [x,y];
        self.feet = pg.Rect(0, 0, self.rect.width // 2, 12)
        self.feet.midbottom = self.rect.midbottom
        self.old_position = self.position.copy()

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


    # comsomation de l'énergie du perso
    def useEnergy(self, energyToConsume: int) -> None:
        if self.energy >= energyToConsume:
            self.energy -= energyToConsume;

    #def recupEnergy(self) -> None:
        # if self.energy < settings.PLAYER_ENERGY_MAX:
            

    # dash du perso
    # TODO ajout la gestion d'énergie
    def dash(self, value: int, walls: list[pg.Rect] | None = None) -> None:
        if self.energy >= player_constants.DASH_ENERGY_CONSUMPTION:
            self.useEnergy(player_constants.DASH_ENERGY_CONSUMPTION);

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
                    move_x = True; # verrouille l'axe x
                elif keypressed == pg.K_d:
                    self._move_axis(self.speed, 0, walls)
                    self.current_dir_x = Direction.RIGHT;
                    move_x = True;
                
            # --- mouvement y
            if not move_y:
                if keypressed == pg.K_z:
                    self._move_axis(0, -self.speed, walls)
                    self.current_dir_y = Direction.UP;
                    move_y = True; # verrouille l'axe y
                elif keypressed == pg.K_s:
                    self._move_axis(0, self.speed, walls)
                    self.current_dir_y = Direction.DOWN;
                    move_y = True;
