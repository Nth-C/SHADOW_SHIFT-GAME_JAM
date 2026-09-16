import pygame as pg

class Sound:
    def __init__(self):
        pg.mixer.init()

        self.sound_hit = pg.mixer.Sound('assets/sounds/hurt.mp3')
        self.sound_death = pg.mixer.Sound('assets/sounds/death.mp3')
        
        self.sound_hit.set_volume(1)
        self.sound_death.set_volume(1)

        pg.mixer.music.load('assets/sounds/music.mp3')
        pg.mixer.music.set_volume(0.5)

    def play_music(self):
        pg.mixer.music.play(-1)

    def play_hit(self):
        self.sound_hit.play()

    def play_death(self):
        self.sound_death.play()