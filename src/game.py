import pygame as pg
import constants.game_states as game_constants
import constants.settings as settings_constants
from enemy import Enemy
from hud.hud import HudManager
from map import Map
from player import Body, Shadow
from scenes.playing import Playing
from screen import Screen
from scroll import Scroll
from scenes.menu import Menu

# TODO essayer de ranger tout les fichier dans des dossiers

# TODO mettre des constants pour tout les string en ecrit en dur
# TODO mettre des constants pour la taille du screen
# TODO essayer de découper le fichier en plusieurs

class Game:
    def __init__(self):
        pg.display.set_caption(settings_constants.NAME_GAME)
        self.screen = Screen();
        self.timer = pg.time.Clock();

        self.state = game_constants.MENU;
        
        self.menu = Menu();
        self.playing = Playing(self.screen)

    def run(self):
        # boucle de jeu
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if self.state == game_constants.MENU:
                    self.state = self.menu.event_menu_state_game(event);
                    
                elif self.state == game_constants.PLAYING:
                   self.playing.event_playing(event)

            if self.state == game_constants.MENU:
                self.menu.draw_menu(self.screen);
            elif self.state == game_constants.PLAYING:
                self.playing.draw();
                self.playing.update();

            self.screen.update()
            self.timer.tick(60)