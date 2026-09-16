import pygame as pg
from pygame.event import Event
import constants.game_states as game_constants
import constants.settings as settings_constants
from screen import Screen
import constants.game_states as game_constants

class Menu:
    def __init__(self):
        pg.font.init()
        self.font_title = pg.font.SysFont("Arial", 50, bold=True)
        self.font_instruction = pg.font.SysFont("Arial", 25)

    # renvoie l'état du jeu (menu, en jeu)
    def event_menu_state_game(self, event: Event) -> str:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            return game_constants.PLAYING;

        return game_constants.MENU;

    def draw_menu(self, screen: Screen) -> None:
        screen.display.fill((20, 20, 40))
                    
        title_surf = self.font_title.render(settings_constants.NAME_GAME, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(1024 // 2, 768 // 3))
        screen.display.blit(title_surf, title_rect)
                
        inst_surf = self.font_instruction.render("Appuyez sur ESPACE pour commencer", True, (0, 255, 200))
        inst_rect = inst_surf.get_rect(center=(1024 // 2, 768 // 2))
        screen.display.blit(inst_surf, inst_rect)

        # TODO faire un bouton quitter