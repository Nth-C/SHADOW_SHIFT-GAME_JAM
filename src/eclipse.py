import pygame as pg

class Eclipse:
    def __init__(self, x, y):
        self.sprite_sheet = pg.image.load('assets/characters/sprite_eclipse.png').convert_alpha()

        self.width = self.sprite_sheet.get_width() // 5
        self.height = self.sprite_sheet.get_height()

        self.images = [
            pg.transform.scale(self.get_image(0, 0), (128, 128)),
            pg.transform.scale(self.get_image(self.width * 1, 0), (128, 128)),
            pg.transform.scale(self.get_image(self.width * 2, 0), (128, 128)),
            pg.transform.scale(self.get_image(self.width * 3, 0), (128, 128)),
            pg.transform.scale(self.get_image(self.width * 4, 0), (128, 128)),
        ]

        self.rect = pg.Rect(x, y, 128, 128)
        self.img_index = 0
        self.is_animating = False
        self.last_update = 0
        self.duration = 2500

    def get_image(self, x, y):
        image = pg.Surface([self.width, self.height], pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.width, self.height))
        return image

    def start_animation(self):
        self.is_animating = True
        self.img_index = 1
        self.last_update = pg.time.get_ticks()

    def update(self):
        if self.is_animating:
            time_now = pg.time.get_ticks()
            if (time_now - self.last_update) >= self.duration:
                if self.img_index <= len(self.images):
                    self.img_index += 1
                    self.last_update = time_now
                else:
                    self.is_animating = False

    def draw(self, surface, scroll):
        eclipse_move = scroll.apply(self.rect)
        surface.blit(self.images[self.img_index], eclipse_move)