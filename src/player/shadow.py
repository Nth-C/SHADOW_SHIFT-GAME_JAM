import pygame as pg
from pygame.event import Event

import constants.player as player_constants
from entity import Entity
from enums.direction import Direction
from player.playable_entity import PlayableEntity

# Dimensions d'une cellule dans la sprite sheet (grille 3x4)
FRAME_W = 255
FRAME_H = 256
DISPLAY_SIZE = (64, 64)
ANIMATION_SPEED = 150  # millisecondes entre chaque frame

class Shadow(PlayableEntity):
    def __init__(self, x: int, y:int):
        super().__init__(x, y)
        self.sprite_sheet = pg.image.load('assets/characters/sprite_shadow.png').convert_alpha()
        
        # Charger les frames pour chaque direction
        face_idle_1 = self._get_frame(1, 1)
        face_idle_2 = self._get_frame(1, 2)
        left_idle = pg.transform.flip(face_idle_1, True, False)
        self.animations = {
            'down':  [self._get_frame(0, 0), self._get_frame(1, 0), self._get_frame(2, 0)],
            'left':  [self._get_frame(0, 1), left_idle, self._get_frame(0, 2), left_idle],
            'right': [self._get_frame(2, 1), face_idle_2, self._get_frame(2, 2), face_idle_2],
            'up':    [self._get_frame(0, 3), self._get_frame(1, 3), self._get_frame(2, 3)],
        }

        # Compatibilité : images statiques (idle)
        self.images = {
            direction: frames[len(frames) // 2] for direction, frames in self.animations.items()
        }

        # État de l'animation
        self.current_animation = 'down'
        self.anim_index = 1
        self.anim_timer = pg.time.get_ticks()
        self.is_moving = False

        self.image = self.animations['down'][1]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.feet = pg.Rect(0, 0, self.rect.width // 2, 12)
        self.feet.midbottom = self.rect.midbottom
        
        self.is_defenseless = False;

        self.keypress_history: list[int] = []; # liste des touche qui sont actuellement presser
        self.current_dir_x: Direction = Direction.RIGHT; # direction dans laquel le joueur est
        self.current_dir_y: Direction = None;
        self.position = [x,y];

        self.speed = 6;

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
        self.is_moving = False