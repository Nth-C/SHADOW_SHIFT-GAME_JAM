import os
from pathlib import Path

import pygame as pg

from game import Game

project_root = Path(__file__).resolve().parent.parent
os.chdir(project_root)

if __name__ == "__main__":
    pg.init()
    game = Game()
    game.run()
