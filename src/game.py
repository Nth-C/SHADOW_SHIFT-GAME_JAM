import sys
import pygame as pg
<<<<<<< HEAD
import constants.game_states as game_constants
=======

from constants.player import HP_MAX
from player import Body
from player import Shadow
>>>>>>> e8c55ed0e235494dd10ca02e9bd1d5dd282a8647
import constants.settings as settings_constants
from hud.hud import HudManager
from map import Map
<<<<<<< HEAD
from player import Body, Shadow
from scenes.playing import Playing
=======
>>>>>>> e8c55ed0e235494dd10ca02e9bd1d5dd282a8647
from screen import Screen
from entity import Entity
from enemy import Enemy
from scroll import Scroll
<<<<<<< HEAD
from scenes.menu import Menu
=======
import constants.game_states as game_constants
import constants.settings as settings_constants
from light import render_lights
>>>>>>> e8c55ed0e235494dd10ca02e9bd1d5dd282a8647

# TODO essayer de ranger tout les fichier dans des dossiers

# TODO mettre des constants pour tout les string en ecrit en dur
# TODO mettre des constantes pour la taille du screen
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
        while running: # boucle pour vérifier si des action ont été réalisé / ne pas mettre d'affichage dedans
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
            self.timer.tick(60);