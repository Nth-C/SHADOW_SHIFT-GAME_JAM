import pygame

class Scroll:
    def __init__(self):
        self.x = 0
        self.y = 0

    def apply(self, rect):
        return rect.move(self.x, self.y)

    def scroll_update(self, target, width, height):
        self.x = -target.rect.centerx + (width // 2)
        self.y = -target.rect.centery + (height // 2)
    