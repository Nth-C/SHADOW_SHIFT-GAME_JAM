import pygame as pg
from pygame.event import Event

import constants.game_states as game_constants
import constants.settings as settings_constants
from player.body import Body
from screen import Screen


class Menu:
    def __init__(self):
        pg.font.init()
        self.font_title = pg.font.SysFont("Arial", 50, bold=True)
        self.font_instruction = pg.font.SysFont("Arial", 25)

    # detect les evenements
    def start_game(self, event: Event) -> str:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            return game_constants.PLAYING

        return game_constants.MENU

    # TODO faire une heal dans Body et l'utiliser ici et au changement de salle

    def restart_game(self, event: Event, player: Body) -> str:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            # regen le joueur
            player.regen_all();

            return game_constants.PLAYING

        return game_constants.GAME_OVER

    def end_game(self, event: Event, player: Body) -> str:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            # regen le joueur
            player.regen_all();

            return game_constants.CREDITS

        return game_constants.END

    def show_credits(self, event: Event) -> str:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            return game_constants.MENU

        return game_constants.CREDITS

    # --- affichage

    # affiche le menu
    def draw_menu(self, screen: Screen):
        screen.display.fill((20, 20, 40))
                        
        title_surf = self.font_title.render(settings_constants.NAME_GAME, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(1024 // 2, 768 // 3))
        screen.display.blit(title_surf, title_rect)
                        
        inst_surf = self.font_instruction.render("Appuyez sur ESPACE pour commencer", True, (0, 255, 200))
        inst_rect = inst_surf.get_rect(center=(1024 // 2, 768 // 2))
        screen.display.blit(inst_surf, inst_rect)

    # affiche l'ecran game over
    def draw_game_over(self, screen: Screen):
        screen.display.fill((20, 20, 40))

        title_surf = self.font_title.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_surf.get_rect(center=(1024 // 2, 768 // 3))
        screen.display.blit(title_surf, title_rect)

        inst_surf = self.font_instruction.render("Appuyez sur ESPACE pour recommencer", True, (255, 0, 0))
        inst_rect = inst_surf.get_rect(center=(1024 // 2, 768 // 2))
        screen.display.blit(inst_surf, inst_rect)

    # affiche l'ecran de fin
    def draw_end(self, screen: Screen):
        screen.display.fill((20, 20, 40))

        title_surf = self.font_title.render("VICTOIRE", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(1024 // 2, 768 // 3))
        screen.display.blit(title_surf, title_rect)

        inst_surf = self.font_instruction.render("Appuyez sur ESPACE pour retourner au menu", True, (0, 255, 200))
        inst_rect = inst_surf.get_rect(center=(1024 // 2, 768 // 2))
        screen.display.blit(inst_surf, inst_rect)

    # affiche l'ecran des credits
    def draw_credits(self, screen: Screen):
        screen.display.fill((20, 20, 40))

        title_surf = self.font_title.render("CREDITS", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(1024 // 2, 768 // 6))
        screen.display.blit(title_surf, title_rect)

        credits_lines = [
            "Realisé par",
            "Rayan Tata, Nathan Coeurdevey,",
            "Mathieu Macaud, Enzo Galiano et Thomas Demarcq",
            "",
            "Assets audio :",
            "Pack audio par Chequered Ink",
        ]

        start_y = 768 // 3
        line_height = 40

        for i, line in enumerate(credits_lines):
            line_surf = self.font_instruction.render(line, True, (0, 255, 200))
            line_rect = line_surf.get_rect(center=(1024 // 2, start_y + i * line_height))
            screen.display.blit(line_surf, line_rect)

        inst_surf = self.font_instruction.render("Appuyez sur ESPACE pour retourner au menu", True, (255, 255, 255))
        inst_rect = inst_surf.get_rect(center=(1024 // 2, 768 - 60))
        screen.display.blit(inst_surf, inst_rect)