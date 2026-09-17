import pygame as pg

import constants.game_states as game_constants
import constants.settings as settings_constants
from scenes.menu import Menu
from scenes.playing import Playing
from screen import Screen


class Game:
    def __init__(self):
        pg.display.set_caption(settings_constants.NAME_GAME)
        self.screen = Screen()
        self.timer = pg.time.Clock()
        
        self.state = game_constants.MENU
        
        self.menu = Menu()
        self.playing = Playing()

    def run(self):
        running = True
        while running:
            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if self.state == game_constants.MENU:
                    self.state = self.menu.start_game(event)
                    if self.state == game_constants.PLAYING:
                        self.playing.respawn_player()
                elif self.state == game_constants.GAME_OVER:
                    self.state = self.menu.restart_game(event, self.playing.player)
                    if self.state == game_constants.PLAYING:
                        self.playing.respawn_player()
                elif self.state == game_constants.END:
                    self.menu.draw_end(self.screen, self.playing.game_timer.get_formatted_time())
                elif self.state == game_constants.CREDITS:
                    self.state = self.menu.show_credits(event)
                elif self.state == game_constants.PLAYING:
                    self.playing.handle_event(event)

            # affichage
            if self.state == game_constants.MENU:
                self.menu.draw_menu(self.screen)
            elif self.state == game_constants.GAME_OVER:
                self.menu.draw_game_over(self.screen)
            elif self.state == game_constants.END:
                self.menu.draw_end(self.screen)
            elif self.state == game_constants.CREDITS:
                self.menu.draw_credits(self.screen)
            elif self.state == game_constants.PLAYING:
                self.state = self.playing.update()
                self.playing.draw()

            # refresh
            self.screen.update()
            self.timer.tick(60)