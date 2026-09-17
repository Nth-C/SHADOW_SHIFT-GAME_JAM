import pygame as pg

from enemy import Enemy


class Boss(Enemy):
    def __init__(self, x: int, y: int, width: int = 128, height: int = 128, hp: int = 200, attack: int = 20, speed: int = 1, aggro_range: int = 300):
        # Initialize the base class but we will override the images
        super().__init__(x, y, width=width, height=height, hp=hp, attack=attack, speed=speed, aggro_range=aggro_range)

        # Load boss sprite sheet (1024x1024, grille 2x2 séparée par traits noirs à x/y=511-512)
        # Layout : (1,1)=face/down, (1,2)=droite/right, (2,1)=gauche/left, (2,2)=dos/up
        original_sheet = pg.image.load('assets/characters/boss_robot_walk.png').convert_alpha()
        self.sprite_sheet = original_sheet

        # Extraire les 4 frames (une par direction) depuis la grille 2x2
        # Chaque case fait 511x511, séparées par 2px de traits noirs (à 511-512)
        # Les traits noirs débordent sur ~3px dans les cases voisines,
        # donc on rogne une marge de MARGIN pixels sur les bords internes
        MARGIN = 5
        cw = 511 - MARGIN  # largeur utile d'une case
        ch = 511 - MARGIN  # hauteur utile d'une case

        frame_down  = self._extract_and_clean(0,          0,          cw, ch)  # case (1,1) face
        frame_right = self._extract_and_clean(513+MARGIN, 0,          cw, ch)  # case (1,2) droite
        frame_left  = self._extract_and_clean(0,          513+MARGIN, cw, ch)  # case (2,1) gauche
        frame_up    = self._extract_and_clean(513+MARGIN, 513+MARGIN, cw, ch)  # case (2,2) dos

        # Chaque direction n'a qu'une seule frame (pas d'animation multi-frame)
        self.animations = {
            'down':  [frame_down],
            'left':  [frame_left],
            'right': [frame_right],
            'up':    [frame_up],
        }

        self.current_direction = 'down'
        self.current_frame = 0

        self.image = self.animations[self.current_direction][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Adjust the feet rect for collision
        self.feet = pg.Rect(0, 0, self.rect.width // 2, 24)
        self.feet.midbottom = self.rect.midbottom

    def _extract_and_clean(self, src_x, src_y, cell_w, cell_h):
        """Extrait une case, supprime le rose et les traits noirs, centre le contenu, et scale."""
        # Extraire la case brute depuis la sprite sheet
        raw = pg.Surface([cell_w, cell_h], pg.SRCALPHA)
        raw.blit(self.sprite_sheet, (0, 0), (src_x, src_y, cell_w, cell_h))

        # Supprimer les pixels roses et noirs (fond + grille)
        # On convertit en PixelArray pour un accès rapide
        px_array = pg.PixelArray(raw)
        for y in range(cell_h):
            for x in range(cell_w):
                color = raw.unmap_rgb(px_array[x, y])
                r, g, b, a = color
                # Rose/magenta : R > 180, G < 80, B > 180
                if r > 180 and g < 80 and b > 180:
                    px_array[x, y] = raw.map_rgb(0, 0, 0, 0)
        del px_array

        # Trouver la bounding box du contenu visible (non-transparent)
        bbox = raw.get_bounding_rect()

        if bbox.width == 0 or bbox.height == 0:
            return pg.transform.scale(raw, (self.width, self.height))

        # Extraire le contenu visible
        content = pg.Surface([bbox.width, bbox.height], pg.SRCALPHA)
        content.blit(raw, (0, 0), bbox)

        # Recentrer le contenu dans une surface carrée de taille cell_w x cell_h
        centered = pg.Surface([cell_w, cell_h], pg.SRCALPHA)
        cx = (cell_w - bbox.width) // 2
        cy = (cell_h - bbox.height) // 2
        centered.blit(content, (cx, cy))

        # Scaler à la taille finale
        return pg.transform.scale(centered, (self.width, self.height))

    def change_animation(self, name):
        if self.current_direction != name:
            self.current_direction = name
            self.current_frame = 0
            self.image = self.animations[self.current_direction][0]

    def update(self, player) -> None:
        attack_range = self.get_aggro_range()

        if player.rect.colliderect(attack_range):
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Move towards player
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed

            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > player.rect.y:
                self.rect.y -= self.speed

            # Determine direction based on dominant axis
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.change_animation('right')
                else:
                    self.change_animation('left')
            else:
                if dy > 0:
                    self.change_animation('down')
                elif dy < 0:
                    self.change_animation('up')

        # Update feet position
        self.feet.midbottom = self.rect.midbottom
