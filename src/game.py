import sys
import pygame as pg
from player import Body
import constants.settings as settings_constants
from hud.hud import HudManager
from map import Map
from screen import Screen

class Game:
    def __init__(self):
        pg.display.set_caption("Shadow of PikPik");

        self.screen = pg.display.set_mode((settings_constants.WIDTH_SCREEN, settings_constants.HEIGHT_SCREEN));
        self.timer = pg.time.Clock();
        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        
        self.player = Body(400, 300);
        self.hud = HudManager()

    def run(self):
        # boucle de jeu
        running = True;
        self.screen = Screen()

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False;
                    
                self.player.event_handler(event);
                
            self.player.move();
            #self.player.recupEnergy();
            
            self.screen.fill((30, 30, 30));
            self.screen.blit(self.player.image, self.player.rect);

            self.hud.draw(self.screen, self.player)
            
            pg.display.flip();
            clock.tick(self.screen.framerate)
            self.screen.update()
            self.map.draw()


        pg.quit();
        sys.exit();
import pygame
