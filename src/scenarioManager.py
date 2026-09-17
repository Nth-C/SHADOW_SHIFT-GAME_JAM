import pygame as pg


class ScenarioManager:
    def __init__(self):
        self.step = 0
        self.wave = 0
        self.dialogs = []
        self.dialogs_index = 0
        self.font_dialogue = pg.font.SysFont("Arial", 22, bold=True)
        self.dialog_played = False
        self.memories = {}

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
        if not self.is_dialog_playing() and game.entity_active == game.player:
            for zone_rect, zone_type in game.walls_dialogs:
                if game.player.feet.colliderect(zone_rect.inflate(15, 15)):
                    
                    if zone_type == 'dialogue 1' and not self.memories.get("read"):
                        self.start_dialog([
                            ("Sujet 0", "Je pourrais utiliser mon ombre pour passer derrière cette grille"),
                            ("Tutoriel", "Appuyez sur [A] pour activer la capacitée spécial du sujet 0\n(Détachement de l'ombre)."),
                            ("Tutoriel", "Puis appuyez sur [c] pour vous téléporter sur votre ombre.")
                        ])
                        self.memories["read"] = True
                        
                    elif zone_type == 'wave_exit' and len(game.enemies) > 0:
                        if not self.memories["touche_wall"]:
                            self.start_dialog([
                                ("Sujet 0", "Je dois d'abord éliminer tous les ennemies de la zone\navant de pouvoir passer à la prochaine."),
                            ])
                            self.memories["touche_wall"] = True

                    elif zone_type == 'dialogue':
                        if self.step == 0 and not self.memories.get("salle1_exit"):
                            self.start_dialog([
                                ("Narrateur", "Enfin libre... Mais la garde de nuit veillait déjà."),
                                ("Sujet 0", "Maintenant il faut que je trouve un moyen d'accéder\nà la salle du soleil pour éteindre la source d'Energie\ndu laboratoire")                            
                            ])
                            self.memories["salle1_exit"] = True
                            
                        elif self.step == 1 and not self.memories.get("salle2_intro"):
                            self.start_dialog([
                                ("Narrateur", "le Sujet 0 pénétra dans ???. L'air y était lourd, étouffant."),
                                ("Narrateur", "Les sentinelles mutantes l'attendaient de pied ferme."),
                            ])
                            self.memories["salle2_intro"] = True
                            self.wave = 1
                            
                        elif self.step == 2 and not self.memories.get("salle3_intro"):
                            self.start_dialog([
                                ("Sujet 0", "Parfait il ne me reste plus qu'a couper cette source\nd'energie et je pourrais partire."),
                                ("Narrateur", "Lorsque le joueur s'approcha une vague de robot lui sauta dessus")
                            ])
                            self.memories["salle3_intro"] = True
                            self.wave = 1

                else:
                    if zone_type == 'wave_exit':
                        self.memories['touche_wall'] = False

        
        if self.step == 0:
            if not self.memories.get("intro_jeu"):
                self.start_dialog([
                    ("Narrateur", "Le Sujet Zéro ouvrit les yeux. Enfermé dans sa chambre."),
                    ("Tutoriel", "Appuyez sur [ESPACE] pour effectuer un Dash (esquive).")
                ])
                self.memories["intro_jeu"] = True

            if len(game.enemies) <= 0 and self.memories.get("salle1_sortie"):
                self.step = 1

        elif self.step == 1:
            if self.wave == 1 and not self.is_dialog_playing():
                if not self.memories.get("s2_wave1"):
                    self.start_dialog([
                        ("Narrateur", "Le Sujet 0 frappa. L'ombre esquiva. Mais la horde\nne faisait que commencer. "),
                    ])
                    # game.enemies.add( Enemy(...) )
                    self.memories["s2_wave1"] = True
                    
                elif len(game.enemies) <= 0 and self.memories.get("s2_w1_spawned"):
                    self.wave = 2

            elif self.wave == 2 and not self.is_dialog_playing():
                if not self.memories.get("s2_wave2"):
                    self.start_dialog([
                        ("Narrateur", "Attention encore des enemies"),
                    ])
                    # game.enemies.add( Enemy(...) )
                    self.memories["s2_wave2"] = True
                    
                elif len(game.enemies) <= 0 and self.memories.get("s2_w2_spawned"):
                    if not self.memories.get("s2_end"):
                        self.start_dialog([
                            ("Sujet 0", "Enfin ça y est il n'y a plus personne."),
                        ])
                        self.memories["s2_end"] = True
                        
                    elif not self.is_dialog_playing():
                        self.wave = 0
                        self.step = 2

        elif self.step == 2:
            if self.wave == 1 and not self.is_dialog_playing():
                if not self.memories.get("s3_wave1"):
                    # game.enemies.add( Enemy(...) )
                    self.memories["s3_wave1"] = True
                elif len(game.enemies) <= 0 and self.memories.get("s3_wave1"):
                    self.wave = 2

            elif self.wave == 2 and not self.is_dialog_playing():
                if not self.memories.get("s3_wave2"):
                    # game.enemies.add( Enemy(...) )
                    self.memories["s3_wave2"] = True
                elif len(game.enemies) <= 0 and self.memories.get("s3_wave2"):
                    self.wave = 3

            elif self.wave == 3 and not self.is_dialog_playing():
                if not self.memories.get("s3_wave_boss"):
                    self.start_dialog([
                        ("Narrateur", "..."),
                        ("Narrateur", "un bruit sours ce rapprocha du joueur")
                    ])
                    # game.enemies.add( Boss(...) )
                    self.memories["s3_wave_boss"] = True
                elif len(game.enemies) <= 0 and self.memories.get("s3_wave_boss"):
                    self.wave = 0
                    self.step = 3

        elif self.step == 3:
            if not self.memories.get("end_wave_boss"):
                self.start_dialog([
                    ("Sujet 0", "J'était à 2 doigt d'y passer, j'ai vraiment eu de la chance."),
                    ("Sujet 0", "Bon maintenant comment éteindre cette source d'energie."),
                    ("Tutoriel", "Pour éteindre le soleil rapprocher vous de lui puis appuyez sur [e].")
                ])
                self.memories["end_wave_boss"] = True
                
            elif not self.is_dialog_playing() and not self.memories.get("eclipse_start"):
                game.eclipse.start_animation()
                self.memories["eclipse_start"] = True
                
            elif self.memories.get("eclipse_start") and not self.is_dialog_playing() and not self.memories.get("conclusion"):
                self.start_dialog([
                    ("Narrateur", "une fois toutes les portes ouverte le sujet 0 ainsi que son\nombre prirent une navette pour partir débuter une nouvelle vie\nloin de toutes cette agitation")
                ])
                self.memories["conclusion"] = True

    def dialog_draw(self, surface):
        if self.is_dialog_playing():
            speaker, text = self.dialogs[self.dialogs_index]

            box_rect = pg.Rect(162, 600, 700, 120)
            pg.draw.rect(surface, (10, 10, 20), box_rect)
            pg.draw.rect(surface, (255, 255, 255), box_rect, 2)

            surface.blit(self.font_dialogue.render(speaker, True, (255, 215, 0)), (182, 610))
            y = 645
            for ligne in text.split('\n'): # Coupe le texte à chaque "\n"
                surface.blit(self.font_dialogue.render(ligne, True, (255, 255, 255)), (182, y))
                y += 25
            surface.blit(self.font_dialogue.render("[ENTRÉE]", True, (150, 150, 150)), (750, 680))