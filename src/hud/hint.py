import pygame as pg
from pygame.event import Event


class Hint:
    def __init__(self, text: str, desable_key: int, is_active: bool = False):
        self.text = text
        self.desable_key = desable_key
        self.is_active = is_active

        pg.font.init()
        self.font = pg.font.SysFont("Arial", 16)

    def handle_event(self, event: Event):
        # ferme l'hint
        if not self.is_active:
            return

        # si on clique sur la touche on sppr l'hint
        if event.type == pg.KEYDOWN and event.key == self.desable_key:
            self.is_active = False

    def draw(self, surface: pg.Surface):
        if not self.is_active:
            return

        # Rendu du texte et du fond
        hint_surf = self.font.render(self.text, True, (255, 255, 255))
        hint_rect = hint_surf.get_rect(midbottom=(1024 // 2, 768 // 3))

        bg_rect = hint_rect.inflate(20, 20)
        bg_surf = pg.Surface(bg_rect.size, pg.SRCALPHA)
        bg_surf.fill((0, 0, 0, 150))
        
        surface.blit(bg_surf, bg_rect)
        surface.blit(hint_surf, hint_rect)