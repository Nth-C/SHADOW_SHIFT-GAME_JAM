import pygame as pg
from pygame.event import Event

import constants.player as player_constants
from entity import Entity
from enums.direction import Direction
from player.playable_entity import PlayableEntity

# Dimensions d'une cellule dans la sprite sheet (765x1024, grille 3x4)
FRAME_W = 255
FRAME_H = 256
DISPLAY_SIZE = (64, 64)
ANIMATION_SPEED = 150  # millisecondes entre chaque frame

class Body(PlayableEntity):
    def __init__(self, x: int, y:int):
        super().__init__(x, y)

        self.sprite_sheet = pg.image.load('assets/characters/sprite_perso.png').convert_alpha()

        # Rangée 0 = down (3 frames), Rangée 3 = up (3 frames)
        # Rangées 1-2 : col 0 = left, col 2 = right
        # Pour gauche/droite : cycle de marche pas1 → neutre → pas2 → neutre
        face_idle_1 = self._get_frame(1, 1)  # sprite face neutre (rangée 1)
        face_idle_2 = self._get_frame(1, 2)  # sprite face neutre (rangée 2)
        left_idle = pg.transform.flip(face_idle_1, True, False)  # miroir pour orienter à gauche
        self.animations = {
            'down':  [self._get_frame(0, 0), self._get_frame(1, 0), self._get_frame(2, 0)],
            'left':  [self._get_frame(0, 1), left_idle, self._get_frame(0, 2), left_idle],
            'right': [self._get_frame(2, 1), face_idle_2, self._get_frame(2, 2), face_idle_2],
            'up':    [self._get_frame(0, 3), self._get_frame(1, 3), self._get_frame(2, 3)],
        }

        # Compatibilité : images statiques (idle = frame du milieu ou frame 0)
        self.images = {
            direction: frames[len(frames) // 2] for direction, frames in self.animations.items()
        }

        # État de l'animation
        self.current_animation = 'down'
        self.anim_index = 1  # frame du milieu = idle
        self.anim_timer = pg.time.get_ticks()
        self.is_moving = False

        self.image = self.animations['down'][1]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.feet = pg.Rect(0, 0, self.rect.width // 2, 12)
        self.feet.midbottom = self.rect.midbottom

        self.position = [x,y];

        self.old_position = self.position.copy()
        self.last_regen_time = pg.time.get_ticks()
        self.capacity_active = False
        self.last_capacity_time = pg.time.get_ticks()

    def _get_frame(self, col: int, row: int) -> pg.Surface:
        """Extrait une frame de la sprite sheet et la redimensionne."""
        frame = pg.Surface((FRAME_W, FRAME_H), pg.SRCALPHA)
        frame.blit(self.sprite_sheet, (0, 0), (col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H))
        return pg.transform.scale(frame, DISPLAY_SIZE)

    def change_animation(self, name):
        """Change la direction de l'animation et active le cycle de marche."""
        if self.current_animation != name:
            self.current_animation = name
            self.anim_index = 0
            self.anim_timer = pg.time.get_ticks()
        self.is_moving = True

    def update_animation(self):
        """Met à jour la frame d'animation en fonction du temps."""
        now = pg.time.get_ticks()
        if self.is_moving:
            if now - self.anim_timer >= ANIMATION_SPEED:
                self.anim_timer = now
                frames = self.animations[self.current_animation]
                self.anim_index = (self.anim_index + 1) % len(frames)
            self.image = self.animations[self.current_animation][self.anim_index]
        else:
            # Idle : frame du milieu pour 3 frames, frame 0 pour 2 frames
            frames = self.animations[self.current_animation]
            self.image = frames[len(frames) // 2]
        self.is_moving = False  # sera remis à True par move() si le joueur bouge

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
