import pygame as pg
from waves import Waves
from boss import Boss
from utils_wave import get_enemies_of_waves
from utils_wave import get_enemies_of_waves

class ScenarioManager:
    def __init__(self):
        self.step = 0
        self.wave = 0
        self.dialogs = []
        self.dialogs_index = 0
        self.font_dialogue = pg.font.SysFont("Arial", 22, bold=True)
        self.dialog_played = False
        self.memories = {}
        self.zone_past = []

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
        was_playing = self.is_dialog_playing()

        if not self.is_dialog_playing():
            for zone_rect, zone_type in game.walls_dialogs:
                if game.entity_active.feet.colliderect(zone_rect.inflate(15, 15)):

                    if zone_rect not in self.zone_past or zone_type == 'wave_exit':
                    
                        if zone_type == 'dialogue 1' and not self.memories.get("read"):
                            self.start_dialog([
                                ("Sujet 0", "Je pourrais utiliser mon ombre pour passer derrière cette grille."),
                                ("Tutoriel", "Appuyez sur [A] pour activer la capacité spéciale du Sujet 0\n(Détachement de l'ombre)."),
                                ("Tutoriel", "Puis appuyez sur [C] pour vous téléporter sur votre ombre.")
                            ])
                            self.memories["read"] = True
                            
                        elif zone_type == 'wave_exit' and len(game.waves.get_current_enemies()) > 0:
                            if not self.memories.get("touche_wall"):
                                self.start_dialog([
                                    ("Sujet 0", "Je dois d'abord éliminer tous les ennemis de la zone\navant de pouvoir passer à la prochaine."),
                                ])
                                self.memories["touche_wall"] = True

                        elif zone_type == 'dialogue':
                            if self.step == 0 and not self.memories.get("salle1_exit"):
                                self.start_dialog([
                                    ("Narrateur", "Enfin libre... Mais la garde de nuit veillait déjà."),
                                    ("Narrateur", "Mais attention, l'ombre et la lumière ne font pas bon ménage."),
                                    ("Sujet 0", "Maintenant, il faut que je trouve un moyen d'accéder\nà la salle du soleil pour éteindre la source d'énergie\ndu laboratoire.")
                                ])
                                self.memories["salle1_exit"] = True
                                self.zone_past.append(zone_rect)
                                
                            elif self.step == 1 and not self.memories.get("salle2_intro"):
                                self.start_dialog([
                                    ("Narrateur", "Le Sujet 0 pénétra dans la salle de recherche. L'air y était\nlourd, étouffant."),
                                    ("Narrateur", "Les robots sentinelles l'attendaient de pied ferme."),
                                ])
                                self.memories["salle2_intro"] = True
                                self.zone_past.append(zone_rect)
                                self.wave = 1
                                
                            elif self.step == 2 and not self.memories.get("salle3_intro"):
                                self.start_dialog([
                                    ("Sujet 0", "Parfait, il ne me reste plus qu'à couper cette source\nd'énergie et je pourrai partir."),
                                    ("Narrateur", "Lorsque le joueur s'approcha, une vague de robots\nlui sauta dessus.")
                                ])
                                self.memories["salle3_intro"] = True
                                self.zone_past.append(zone_rect)
                                self.wave = 1

                                game.spawn_entities_at_sun()

                else:
                    if zone_type == 'wave_exit':
                        self.memories['touche_wall'] = False

        
        if self.step == 0:
            if not self.memories.get("intro_jeu"):
                self.start_dialog([
                    ("Narrateur", "Le Sujet 0 ouvrit les yeux. Enfermé dans sa chambre."),
                    ("Tutoriel", "Appuyez sur [ESPACE] pour effectuer un Dash (esquive).")
                ])
                self.memories["intro_jeu"] = True
            
            if len(game.waves.get_current_enemies()) <= 0 and self.memories.get("salle1_exit"):
                self.step = 1

        elif self.step == 1:
            if self.wave == 1 and not self.is_dialog_playing():
                if not self.memories.get("s2_wave1"):
                    self.start_dialog([
                        ("Narrateur", "Le Sujet 0 frappa. L'ombre esquiva. Mais la horde\nne faisait que commencer."),
                    ])
                    game.waves.list_of_waves.append(get_enemies_of_waves(game, 1, 14, 4))
                    game.waves.list_of_waves.append(get_enemies_of_waves(game, 1, 14, 4))

                    game.waves.is_active = True
                    self.memories["s2_wave1"] = True
                    
                elif len(game.waves.get_current_enemies()) <= 0 and self.memories.get("s2_wave1"):
                    self.wave = 2

            elif self.wave == 2 and not self.is_dialog_playing():
                if not self.memories.get("s2_wave2"):
                    self.start_dialog([
                        ("Narrateur", "Attention, encore des ennemis."),
                    ])
                    
                    game.waves.is_active = True
                    self.memories["s2_wave2"] = True
                    
                elif len(game.waves.get_current_enemies()) <= 0 and self.memories.get("s2_wave2"):
                    if not self.memories.get("s2_end"):
                        self.start_dialog([
                            ("Sujet 0", "Enfin ça y est, il n'y a plus personne."),
                        ])
                        self.memories["s2_end"] = True
                        
                    elif not self.is_dialog_playing():
                        self.wave = 0
                        self.step = 2

        elif self.step == 2:
            if self.wave == 1 and not self.is_dialog_playing():
                if not self.memories.get("s3_wave1"):
                    game.waves.list_of_waves.append(get_enemies_of_waves(game, 1, 7, 3))
                    game.waves.is_active = True
                    self.memories["s3_wave1"] = True
                elif len(game.waves.get_current_enemies()) <= 0 and self.memories.get("s3_wave1"):
                    self.wave = 2

            elif self.wave == 2 and not self.is_dialog_playing():
                if not self.memories.get("s3_wave2"):
                    game.waves.list_of_waves.append(get_enemies_of_waves(game, 1, 7, 4))
                    game.waves.is_active = True
                    self.memories["s3_wave2"] = True
                elif len(game.waves.get_current_enemies()) <= 0 and self.memories.get("s3_wave2"):
                    self.wave = 3

            elif self.wave == 3 and not self.is_dialog_playing():
                if not self.memories.get("s3_wave_boss"):
                    self.start_dialog([
                        ("Narrateur", "..."),
                        ("Narrateur", "Un bruit sourd se rapprocha du joueur.")
                    ])
                    
                    boss_obj = game.map.tmx_data.get_object_by_name("boss")
                    boss_wave = pg.sprite.Group()
                    boss_wave.add(Boss(boss_obj.x, boss_obj.y, 128, 128))
                    
                    game.waves.list_of_waves.append(boss_wave)
                    game.waves.is_active = True
                    self.memories["s3_wave_boss"] = True
                elif len(game.waves.get_current_enemies()) <= 0 and self.memories.get("s3_wave_boss"):
                    self.wave = 0
                    self.step = 3

        elif self.step == 3:
            if not self.memories.get("end_wave_boss"):
                self.start_dialog([
                    ("Sujet 0", "J'étais à deux doigts d'y passer, j'ai vraiment eu de la chance."),
                    ("Sujet 0", "Bon maintenant, comment éteindre cette source d'énergie ?"),
                    ("Tutoriel", "Pour éteindre le soleil, rapprochez-vous de lui puis\nappuyez sur [E].")
                ])
                self.memories["end_wave_boss"] = True
                
            elif not self.is_dialog_playing() and not self.memories.get("eclipse_start"):
                keys = pg.key.get_pressed()
                if keys[pg.K_e]:
                    game.eclipse.start_animation()
                    self.memories["eclipse_start"] = True
                
            elif self.memories.get("eclipse_start") and not self.is_dialog_playing() and not self.memories.get("conclusion"):
                self.start_dialog([
                    ("Narrateur", "Une fois toutes les portes ouvertes, le Sujet 0 ainsi que son\nombre prirent une navette pour partir débuter une nouvelle vie\nloin de toute cette agitation.")
                ])
                self.memories["conclusion"] = True

            elif self.memories.get("conclusion") and not self.is_dialog_playing():
                self.step = 4



        if not was_playing and self.is_dialog_playing(): 
                game.player.reset_movement()
                game.shadow.reset_movement()

    def dialog_draw(self, surface):
        if self.is_dialog_playing():
            speaker, text = self.dialogs[self.dialogs_index]

            box_rect = pg.Rect(162, 600, 700, 140)
            pg.draw.rect(surface, (10, 10, 20), box_rect)
            pg.draw.rect(surface, (255, 255, 255), box_rect, 2)

            surface.blit(self.font_dialogue.render(speaker, True, (255, 215, 0)), (182, 610))
            y = 645
            for ligne in text.split('\n'): 
                surface.blit(self.font_dialogue.render(ligne, True, (255, 255, 255)), (182, y))
                y += 25
            surface.blit(self.font_dialogue.render("[ENTRÉE]", True, (150, 150, 150)), (750, 680))

    def reset(self):
        self.step = 0
        self.wave = 0
        self.dialogs = []
        self.dialogs_index = 0
        self.dialog_played = False
        self.memories = {}
        self.zone_past = []