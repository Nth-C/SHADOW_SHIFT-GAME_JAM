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

        self.screen = Screen()
        self.timer = pg.time.Clock();
        
        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        
        self.player = Body(400, 300);
        self.hud = HudManager()

    def run(self):
        # boucle de jeu
        running = True;

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False;
                    
                self.player.event_handler(event);
                
            self.player.move();
            #self.player.recupEnergy();

            self.map.draw()
            
            self.screen.display.blit(self.player.image, self.player.rect)
            self.hud.draw(self.screen.display, self.player)

            self.screen.update()
            self.timer.tick(60)

        pg.quit();
        sys.exit();