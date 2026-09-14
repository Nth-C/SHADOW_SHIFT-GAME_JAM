import pygame
from Entity import Entity
from enums.direction import Direction
 
class Body(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 255, 0), size=50, hp=100, attack=20, speed=4)
        self.is_defenseless = False

    def dash(self, value: int, direction: Direction):
        if direction == Direction.UP:
            self.rect.y -= value
        elif direction == Direction.DOWN:
            self.rect.y += value
        elif direction == Direction.LEFT:
            self.rect.x -= value
        elif direction == Direction.RIGHT:
            self.rect.x += value


    def move(self, touches):
        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            self.rect.x -= self.speed
            if touches[pygame.K_SPACE]:
                self.dash(10, Direction.LEFT)

        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            self.rect.x += self.speed
            if touches[pygame.K_SPACE]:
                self.dash(10, Direction.RIGHT)

        if touches[pygame.K_UP] or touches[pygame.K_z]:
            self.rect.y -= self.speed
            if touches[pygame.K_SPACE]:
                self.dash(10, Direction.UP)

        if touches[pygame.K_DOWN] or touches[pygame.K_s]:
            self.rect.y += self.speed
            if touches[pygame.K_SPACE]:
                self.dash(10, Direction.DOWN)

