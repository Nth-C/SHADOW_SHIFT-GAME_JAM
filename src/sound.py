import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()

        self.sound_hit = pg.mixer.Sound('assets/sounds/hurt.wav')
        self.sound_death = pg.mixer.Sound('assets/sounds/lose.wav')
        self.sound_attack = pg.mixer.Sound('assets/sounds/punch.wav')
        self.sound_enemy_death = pg.mixer.Sound('assets/sounds/robot_death.wav')
        self.sound_shadow_enter = pg.mixer.Sound('assets/sounds/become_shadow.wav')
        self.sound_shadow_exit = pg.mixer.Sound('assets/sounds/power_down.wav')

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

    def play_attack(self):
        self.sound_attack.play()

    def play_enemy_death(self):
        self.sound_enemy_death.play()

    def play_shadow_enter(self):
        self.sound_shadow_enter.play()

    def play_shadow_exit(self):
        self.sound_shadow_exit.play()
