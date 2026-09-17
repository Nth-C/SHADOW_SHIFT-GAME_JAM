import os
from pathlib import Path
import pygame as pg

project_root = Path(__file__).resolve().parent.parent
os.chdir(project_root)

from game import Game

if __name__ == '__main__':
    pg.init();
    game = Game();
    game.run()
