import pygame as pg


class ScenarioManager:
    def __init__(self):
        self.step = 0
        self.wave = 0
        self.dialogs = []
        self.dialogs_index = 0
        self.font_dialogue = pg.font.SysFont("Arial", 22, bold=True)

    def is_dialog_playing(self):
        return len(self.dialogs) > 0

    def start_dialog(self, dialog_liste):
        self.dialogs = dialog_liste
        self.dialogs_index = 0

    def event_handler(self, event):
        if self.is_dialog_playing():
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.dialogs_index += 1
                if self.dialogs_index >= len(self.dialogs):
                    self.dialogs = []

    def update_dialog(self, game):
        if self.step == 0:
            self.start_dialog([
                ("Narrateur", "Le Sujet Zéro ouvrit les yeux. Enfermé dans ça chambre."),
                ("Tutoriel", "Appuyez sur [ESPACE] pour effectuer un Dash (esquive).")
            ])
            self.step = 1
        elif self.step == 1 and not self.is_dialog_playing() and len(game.enemies) <= 0:
            if self.wave == 0:
                game.enemies.add()
                self.wave = 1
            
            elif self.wave == 1 and len(game.enemies) <= 0:
                game.enemies.add()
                self.wave = 0

            self.step = 2

        elif self.step == 2 and self.wave == 0 and not self.is_dialog_playing() and len(game.enemies) <= 0:
            if self.wave == 0:
                game.enemies.add()
                self.wave = 1
            
            elif self.wave == 1 and len(game.enemies) <= 0:
                game.enemies.add()
                self.wave = 0

            self.step = 3

        elif self.step == 3 and self.wave == 0 and not self.is_dialog_playing() and len(game.enemies) <= 0:
            if self.wave == 0:
                game.enemies.add()
                self.wave = 1
            
            elif self.wave == 1 and len(game.enemies) <= 0:
                game.enemies.add()
                self.wave = 0

            self.step = 4
        elif self.step == 3 and self.wave == 0 and not self.is_dialog_playing() and len(game.enemies) <= 0:
            game.eclipse.start_animation()

    def dialog_draw(self, surface):
        if self.is_dialog_playing():
            speaker, text = self.dialogs[self.dialogs_index]

            box_rect = pg.Rect(162, 600, 700, 120)
            pg.draw.rect(surface, (10, 10, 20), box_rect)
            pg.draw.rect(surface, (255, 255, 255), box_rect, 2)

            surface.blit(self.font_dialogue.render(speaker, True, (255, 215, 0)), (182, 610))
            surface.blit(self.font_dialogue.render(text, True, (255, 255, 255)), (182, 645))
            surface.blit(self.font_dialogue.render("[ENTRÉE]", True, (150, 150, 150)), (750, 680))