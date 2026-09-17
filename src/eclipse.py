import pygame as pg


class Eclipse:
    def __init__(self, x, y):
        self.sprite_sheet = pg.image.load('assets/characters/sprite_eclipse.png').convert_alpha()

        self.width = self.sprite_sheet.get_width() // 5
        self.height = self.sprite_sheet.get_height()

        self.images = [
            pg.transform.scale(self.get_image(0, 0), (256, 256)),
            pg.transform.scale(self.get_image(self.width * 1, 0), (256, 256)),
            pg.transform.scale(self.get_image(self.width * 2, 0), (256, 256)),
            pg.transform.scale(self.get_image(self.width * 3, 0), (256, 256)),
            pg.transform.scale(self.get_image(self.width * 4, 0), (256, 256)),
        ]

        self.rect = pg.Rect(0, 0, 256, 256)
        self.rect.center = (x, y)
        self.img_index = 0
        self.is_animating = False
        self.last_update = 0
        self.duration = 2500

        self.black_progress = 0
        self.black_progress_start = 0
        self.fade = 0

    def get_image(self, x, y):
        image = pg.Surface([self.width, self.height], pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.width, self.height))
        return image

    def start_animation(self):
        self.is_animating = True
        self.img_index = 1
        self.last_update = pg.time.get_ticks()
        self.black_progress_start = pg.time.get_ticks()

    def update(self):
        if self.is_animating:
            time_now = pg.time.get_ticks()

            time_pass = time_now - self.black_progress_start
            time_animation = self.duration * len(self.images)

            ratio = min(1.0, time_pass / time_animation)
            self.fade = (255 * ratio)

            if (time_now - self.last_update) >= self.duration:
                if self.img_index < len(self.images) - 1:
                    self.img_index += 1
                    self.last_update = time_now
                else:
                    self.is_animating = False

    def draw(self, surface, scroll):
        eclipse_move = scroll.apply(self.rect)
        if self.img_index < len(self.images):
            surface.blit(self.images[self.img_index], eclipse_move)

    def reset(self):
        self.img_index = 0
        self.is_animating = False
        self.last_update = 0
        self.fade = 0